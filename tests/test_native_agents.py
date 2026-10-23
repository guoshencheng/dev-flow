"""Behavioral checks use temporary user directories; never register real agents."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
from urllib.parse import unquote

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import native_agents as native
from sync_host_agents import LINK


class AgentNameTests(unittest.TestCase):
    def test_supported_root_names(self):
        samples = [
            'name = "dev_product" # comment\n',
            "'name' = 'dev_product'\n",
            r'"\u006eame" = "dev_\u0070roduct"' + '\n',
            r'name = "dev_\U00000070roduct"' + '\n',
            'name = """\ndev_product"""\n',
            "name = '''\ndev_product'''\n",
            'name = """dev_\\\n   product"""\n',
        ]
        for source in samples:
            with self.subTest(source=source):
                self.assertEqual(native.agent_name(source), 'dev_product')

    def test_nested_and_instruction_text_are_not_root_names(self):
        source = '''# name = "dev_product"
description = "[fake] name = 'dev_product'"
developer_instructions = """
[fake]
name = "dev_product"
"""
values = [
  "name = 'dev_product'", { name = "dev_product" }
]
name = 'custom'
[nested]
name = 'dev_product'
'''
        self.assertEqual(native.agent_name(source), 'custom')

    def test_uncertain_names_fail_closed(self):
        for source in [
            'name="one"\nname="two"',
            'name="bad\\q"', 'name="bad\\u12"',
            'name="unterminated', 'values=[\nname="dev_product"',
            'name = 3', '[nested]\nname="dev_product"',
            'name.part = "dev_product"', '"""name"""="custom"',
            'name="bad\\uD800"',
        ]:
            with self.subTest(source=source):
                with self.assertRaises(ValueError):
                    native.agent_name(source)


class NativeAgentTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.base = Path(self.temporary.name)
        self.environment = patch.dict(os.environ, {'CODEX_HOME': str(self.base / 'codex home')})
        self.environment.start()
        self.source = self.base / 'source'
        self.source.mkdir()
        self.cached = self.base / 'cache (version) # > 中文'
        self.cached.mkdir()
        root = Path(__file__).resolve().parents[1]
        # Only role/link resources are needed for these focused file tests.
        for directory in ('agents', 'skills'):
            shutil.copytree(root / directory, self.cached / directory,
                            ignore=shutil.ignore_patterns('node_modules', 'dist', '__pycache__'))
        self.manager = native.NativeAgents(self.source)
        self.record = self.source / '.dev-flow/plugin-install.json'

    def tearDown(self):
        self.environment.stop()
        self.temporary.cleanup()

    def install(self):
        with self.manager.locked():
            _, snapshot = self.manager.preflight()
            return self.manager.register(self.cached, snapshot, self.record, {'plugin_root': str(self.cached)})

    def test_install_repeat_check_and_links_under_special_path(self):
        self.assertEqual(self.install()['count'], 6)
        self.install()
        with self.manager.locked():
            self.assertEqual(self.manager.check(self.cached)['count'], 6)
        links = 0
        for filename in native.FILES:
            source = (self.manager.agents / filename).read_text()
            self.assertEqual(native.agent_name(source), filename[:-5])
            self.assertNotIn('\nmodel =', source)
            body = json.loads(next(line.partition(' = ')[2] for line in source.splitlines()
                                   if line.startswith('developer_instructions = ')))
            for match in LINK.finditer(body):
                target = match.group(1)
                if not target.startswith('<'):
                    continue
                encoded = target[1:-1].partition('#')[0]
                resolved = Path(unquote(encoded))
                self.assertTrue(resolved.exists(), resolved)
                self.assertTrue(resolved.is_relative_to(self.cached.resolve()), resolved)
                self.assertNotIn(' ', encoded)
                self.assertNotIn('(', encoded)
                self.assertNotIn('>', encoded)
                links += 1
        self.assertGreater(links, 30)

    def test_upgrade_updates_all_resource_paths_and_keeps_other_configuration(self):
        self.install()
        custom = self.manager.agents / 'custom.toml'
        custom.write_text('name="custom"\ndeveloper_instructions="keep"\n')
        old = {name: (self.manager.agents / name).read_bytes() for name in native.FILES}
        destination = self.base / 'cache-next'
        self.cached.rename(destination)
        self.cached = destination
        self.install()
        self.assertEqual(custom.read_text(), 'name="custom"\ndeveloper_instructions="keep"\n')
        for name in native.FILES:
            self.assertNotEqual((self.manager.agents / name).read_bytes(), old[name])
        self.assertEqual(self.manager.check(destination)['count'], 6)

    def test_unowned_modified_and_linked_targets_are_preserved(self):
        self.manager.agents.mkdir(parents=True)
        target = self.manager.agents / native.FILES[0]
        target.write_text('personal')
        with self.assertRaisesRegex(ValueError, '冲突'):
            self.install()
        self.assertEqual(target.read_text(), 'personal')
        target.unlink()
        self.install()
        target.write_text('modified')
        for removing in (False, True):
            with self.assertRaises(ValueError):
                self.manager.preflight(removing=removing)
        target.unlink()
        target.symlink_to(self.cached / 'agents' / native.FILES[0])
        with self.assertRaisesRegex(ValueError, '普通文件'):
            self.install()

    def test_different_filename_same_name_is_conflict(self):
        self.manager.agents.mkdir(parents=True)
        custom = self.manager.agents / 'personal.toml'
        custom.write_text(r'"name" = "dev_\u0070roduct"' + '\n')
        with self.assertRaisesRegex(ValueError, '名称冲突'):
            self.install()
        self.assertFalse(self.record.exists())

    def test_missing_roles_are_detected_and_repaired(self):
        self.install()
        (self.manager.agents / native.FILES[0]).unlink()
        with self.assertRaisesRegex(ValueError, '缺失'):
            self.manager.check(self.cached)
        self.install()
        self.assertEqual(self.manager.check(self.cached)['count'], 6)

    def test_file_error_rolls_back_entire_registration_and_record(self):
        self.install()
        paths = [self.manager.agents / name for name in native.FILES] + [self.manager.state, self.record]
        previous = {path: path.read_bytes() for path in paths}
        upgraded_cache = self.base / 'new-cache-for-rollback'
        shutil.copytree(self.cached, upgraded_cache)
        self.assertNotEqual(native.render_agents(upgraded_cache)[native.FILES[0]], previous[paths[0]])
        original = native.atomic_bytes
        for failure_at in (4, 7, 8):
            calls = []
            def fail_once(path, content):
                calls.append(path)
                if len(calls) == failure_at:
                    raise OSError('simulated full disk')
                original(path, content)
            with self.manager.locked():
                _, snapshot = self.manager.preflight()
                with patch.object(native, 'atomic_bytes', side_effect=fail_once):
                    with self.assertRaisesRegex(ValueError, '重新运行 install'):
                        self.manager.register(upgraded_cache, snapshot, self.record, {'changed': True})
            self.assertEqual({path: path.read_bytes() for path in paths}, previous)
        self.cached = upgraded_cache
        self.install()

    def test_first_install_error_leaves_no_owned_files_and_can_retry(self):
        original = native.atomic_bytes
        for failure_at in (4, 7, 8):
            calls = []
            def fail_once(path, content):
                calls.append(path)
                if len(calls) == failure_at:
                    raise OSError('registration failure')
                original(path, content)
            with patch.object(native, 'atomic_bytes', side_effect=fail_once):
                with self.assertRaises(ValueError):
                    self.install()
            self.assertFalse(self.manager.state.exists())
            self.assertFalse(self.record.exists())
            self.assertFalse(any((self.manager.agents / name).exists() for name in native.FILES))
        self.install()

    def test_changes_during_cli_are_not_overwritten(self):
        self.install()
        _, snapshot = self.manager.preflight()
        target = self.manager.agents / native.FILES[0]
        target.write_text('edited while CLI runs')
        with self.assertRaises(ValueError):
            self.manager.register(self.cached, snapshot, self.record, {})
        self.assertEqual(target.read_text(), 'edited while CLI runs')

    def test_remove_owned_only_and_idempotent(self):
        self.install()
        custom = self.manager.agents / 'custom.toml'
        custom.write_text('name="custom"')
        (self.manager.agents / native.FILES[0]).unlink()
        with self.manager.locked():
            _, snapshot = self.manager.preflight(removing=True)
            self.manager.remove(snapshot, self.record)
            _, snapshot = self.manager.preflight(removing=True)
            self.manager.remove(snapshot, self.record)
        self.assertEqual(list(self.manager.agents.iterdir()), [custom])
        self.assertFalse(self.manager.state.exists())
        self.assertFalse(self.record.exists())

    def test_registry_foreign_source_and_malformed_shape_are_rejected(self):
        self.install()
        with self.assertRaisesRegex(ValueError, '其他来源'):
            native.NativeAgents(self.base / 'foreign').preflight()
        state = json.loads(self.manager.state.read_text())
        state['files'] = list(native.FILES)
        self.manager.state.write_text(json.dumps(state))
        with self.assertRaises(ValueError):
            self.manager.preflight()

    def test_directories_and_registry_cannot_be_links(self):
        self.manager.home.mkdir(parents=True)
        elsewhere = self.base / 'elsewhere'
        elsewhere.mkdir()
        self.manager.agents.symlink_to(elsewhere)
        with self.assertRaisesRegex(ValueError, '目录'):
            self.install()
        self.manager.agents.unlink()
        self.install()
        self.manager.state.unlink()
        self.manager.state.symlink_to(self.record)
        with self.assertRaisesRegex(ValueError, '普通文件'):
            self.manager.preflight()

    def test_lock_serializes_this_tool(self):
        with self.manager.locked():
            with self.assertRaisesRegex(ValueError, '另一个'):
                with native.NativeAgents(self.source).locked():
                    pass

    def test_lock_rejects_an_independent_process_then_allows_retry(self):
        script = ("import sys; sys.path.insert(0, 'scripts'); "
                  "from native_agents import NativeAgents; "
                  "manager=NativeAgents(sys.argv[1]); "
                  "context=manager.locked(); context.__enter__(); context.__exit__(None,None,None)")
        with self.manager.locked():
            result = subprocess.run([sys.executable, '-c', script, str(self.source)],
                                    capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('另一个', result.stderr)
        result = subprocess.run([sys.executable, '-c', script, str(self.source)],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.install()

    def test_remove_failure_rolls_back_files_and_allows_reinstall(self):
        self.install()
        paths = [self.manager.agents / name for name in native.FILES] + [self.manager.state, self.record]
        previous = {path: path.read_bytes() for path in paths}
        original = Path.unlink
        for failure_at in (3, 7, 8):
            calls = []
            def fail_once(path, *args, **kwargs):
                calls.append(path)
                if len(calls) == failure_at:
                    raise OSError('simulated deletion failure')
                return original(path, *args, **kwargs)
            with self.manager.locked():
                _, snapshot = self.manager.preflight(removing=True)
                with patch.object(Path, 'unlink', new=fail_once):
                    with self.assertRaises(ValueError):
                        self.manager.remove(snapshot, self.record)
            self.assertEqual({path: path.read_bytes() for path in paths}, previous)
            self.install()


if __name__ == '__main__':
    unittest.main()
