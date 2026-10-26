"""隔离验证插件打包、缓存核验及用户配置不变。"""
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import manage_plugin as manager


class PluginPackageTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.base = Path(self.temp.name)
        self.environment = patch.dict(os.environ, {'CODEX_HOME': str(self.base / 'codex')})
        self.environment.start()
        self.root = self.base / 'repo'
        self.root.mkdir()
        source = Path(__file__).resolve().parents[1]
        # 夹具与实际打包使用相同源码边界，排除本机旧目录、依赖和构建物。
        for relative in manager.tracked(source):
            target = self.root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source / relative, target)
        self.version = json.loads((self.root / 'plugin.json').read_text())['version']
        self.other_version = self.version + '-stale'
        subprocess.run(['git', 'init', '-q', str(self.root)], check=True)
        subprocess.run(['git', 'add', '.'], cwd=self.root, check=True)
        subprocess.run(['git', '-c', 'user.name=Test', '-c', 'user.email=test@example.com', 'commit', '-qm', 'fixture'], cwd=self.root, check=True)

    def tearDown(self):
        self.environment.stop()
        self.temp.cleanup()

    def test_package_without_setup_and_rebuild(self):
        result = manager.build(self.root)
        bundle = Path(result['build_root'])
        expected_skills = json.loads((self.root / 'capabilities.json').read_text())['skills']
        self.assertEqual(manager.validate_bundle(bundle), expected_skills)
        self.assertIn('iteration-closeout', expected_skills)
        closeout_skill = 'skills/iteration-closeout/SKILL.md'
        self.assertEqual((bundle / closeout_skill).read_bytes(), (self.root / closeout_skill).read_bytes())
        self.assertFalse((bundle / 'skills/dev-flow-setup').exists())
        self.assertFalse((bundle / 'scripts/setup_plugin.py').exists())
        original = result['package_hash']
        skill = self.root / 'skills/dev-flow/SKILL.md'
        skill.write_text(skill.read_text() + '\nchanged\n')
        self.assertNotEqual(manager.build(self.root)['package_hash'], original)

    def test_tampered_cache_is_rejected(self):
        bundle = Path(manager.build(self.root)['build_root'])
        (bundle / 'skills/dev-flow/SKILL.md').write_text('tampered')
        with self.assertRaises(ValueError):
            manager.validate_bundle(bundle)

    def test_stage_checker_and_example_survive_packaging(self):
        source = Path(__file__).resolve().parents[1]
        names = ['skills/dev-flow/scripts/check_iteration.py',
                 'skills/dev-flow/references/stage-state.md',
                 'skills/dev-flow/assets/examples/iteration-state.md']
        for name in names:
            target = self.root / name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source / name, target)
        subprocess.run(['git', 'add', '--'] + names, cwd=self.root, check=True)
        bundle = Path(manager.build(self.root)['build_root'])
        inventory = json.loads((bundle / 'package-files.json').read_text())
        for name in names:
            self.assertIn(name, inventory['files'])
            self.assertEqual((source / name).read_bytes(), (bundle / name).read_bytes())
        example = bundle / 'skills/dev-flow/assets/examples/iteration-state.md'
        result = subprocess.run([sys.executable, str(bundle / names[0]), str(example),
                                 '--root', str(example.parent)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(json.loads(result.stdout)['can_finish'])

    def test_inventory_cannot_reference_outside_bundle(self):
        bundle = Path(manager.build(self.root)['build_root'])
        outside = self.base / 'outside'
        outside.write_text('secret')
        inventory = bundle / 'package-files.json'
        value = json.loads(inventory.read_text())
        value['files'][str(outside)] = manager.digest(outside)
        inventory.write_text(json.dumps(value))
        with self.assertRaises(ValueError):
            manager.validate_bundle(bundle)

    def test_install_check_remove_preserve_user_configuration(self):
        personal = self.base / 'personal'
        self.environment.stop()
        self.environment = patch.dict(os.environ, {'CODEX_HOME': str(personal)})
        self.environment.start()
        (personal / 'agents').mkdir(parents=True)
        guide = personal / 'AGENTS.md'
        guide.write_text('已有流程指引')
        role = personal / 'agents/custom.toml'
        role.write_text('name = "custom"\ndeveloper_instructions = "用户角色"\n')
        cached = self.base / 'cache'
        entry = {'pluginId': manager.PLUGIN_ID, 'enabled': True, 'version': self.version,
                 'source': {'path': str(self.root / '.dev-flow/plugin-source')}}
        present = []
        def fake_cli(args):
            if args == ['plugin', 'marketplace', 'list']:
                return {'marketplaces': []}
            if args[:2] == ['plugin', 'add']:
                shutil.copytree(self.root / '.dev-flow/plugin-source', cached)
                present.append(entry)
                return {'installedPath': str(cached)}
            if args == ['plugin', 'list', '--marketplace', manager.MARKETPLACE]:
                return {'installed': present}
            if args[:2] == ['plugin', 'remove']:
                present.clear()
            return {}
        with patch.object(manager, 'cli', side_effect=fake_cli), patch.object(Path, 'home', return_value=personal):
            installed = manager.install(self.root)
            expected_skills = json.loads((self.root / 'capabilities.json').read_text())['skills']
            self.assertEqual(installed['skills'], len(expected_skills))
            self.assertEqual(installed['native_agents']['count'], 6)
            self.assertEqual(len(list((personal / 'agents').glob('dev_*.toml'))), 6)
            self.assertTrue(manager.check(self.root)['source_matches_cache'])
            manager.remove(self.root)
        self.assertEqual(guide.read_text(), '已有流程指引')
        self.assertEqual(role.read_text(), 'name = "custom"\ndeveloper_instructions = "用户角色"\n')
        self.assertEqual(list((personal / 'agents').iterdir()), [role])
        self.assertFalse((personal / 'dev-flow/native-agents.json').exists())
        self.assertFalse((self.root / '.dev-flow/plugin-install.json').exists())

    def test_foreign_marketplace_stops_install(self):
        with patch.object(manager, 'cli', return_value={'marketplaces': [{'name': manager.MARKETPLACE, 'root': str(self.base / 'foreign')}]}):
            with self.assertRaises(ValueError):
                manager.install(self.root)
        self.assertFalse((self.root / '.dev-flow/plugin-source').exists())

    def test_native_conflict_stops_before_plugin_cli(self):
        personal = self.base / 'codex/agents'
        personal.mkdir(parents=True)
        target = personal / 'dev_product.toml'
        target.write_text('personal role')
        with patch.object(manager, 'cli') as command:
            with self.assertRaisesRegex(ValueError, '冲突'):
                manager.install(self.root)
        command.assert_not_called()
        self.assertEqual(target.read_text(), 'personal role')

    def test_corrupt_installed_cache_does_not_register_roles(self):
        cached = self.base / 'cache'
        def fake_cli(args):
            if args == ['plugin', 'marketplace', 'list']:
                return {'marketplaces': []}
            if args[:2] == ['plugin', 'add']:
                shutil.copytree(self.root / '.dev-flow/plugin-source', cached)
                (cached / 'agents/dev_product.toml').write_text('tampered')
                return {'installedPath': str(cached)}
            if args == ['plugin', 'list', '--marketplace', manager.MARKETPLACE]:
                return {'installed': [{'pluginId': manager.PLUGIN_ID, 'enabled': True}]}
            return {}
        with patch.object(manager, 'cli', side_effect=fake_cli):
            with self.assertRaisesRegex(ValueError, '内容不匹配'):
                manager.install(self.root)
        self.assertFalse((self.base / 'codex/agents/dev_product.toml').exists())
        self.assertFalse((self.root / '.dev-flow/plugin-install.json').exists())

    def test_modified_owned_role_stops_remove_before_plugin_cli(self):
        cached = Path(manager.build(self.root)['build_root'])
        from native_agents import NativeAgents
        registry = NativeAgents(self.root)
        with registry.locked():
            _, snapshot = registry.preflight()
            registry.register(cached, snapshot, self.root / '.dev-flow/plugin-install.json', {})
        (registry.agents / 'dev_product.toml').write_text('edited')
        with patch.object(manager, 'cli') as command:
            with self.assertRaisesRegex(ValueError, '修改'):
                manager.remove(self.root)
        command.assert_not_called()
        self.assertTrue(registry.state.exists())

    def test_active_version_and_source_must_match_before_registration(self):
        cached = self.base / 'cache'
        entry = {'pluginId': manager.PLUGIN_ID, 'enabled': True, 'version': self.other_version,
                 'source': {'path': str(self.root / '.dev-flow/plugin-source')}}
        def fake_cli(args):
            if args == ['plugin', 'marketplace', 'list']:
                return {'marketplaces': []}
            if args[:2] == ['plugin', 'add']:
                shutil.copytree(self.root / '.dev-flow/plugin-source', cached, dirs_exist_ok=True)
                return {'installedPath': str(cached)}
            if args == ['plugin', 'list', '--marketplace', manager.MARKETPLACE]:
                return {'installed': [entry]}
            return {}
        with patch.object(manager, 'cli', side_effect=fake_cli):
            for version in (self.other_version, None):
                entry['version'] = version
                with self.assertRaisesRegex(ValueError, '版本'):
                    manager.install(self.root)
                self.assertFalse((self.base / 'codex/agents/dev_product.toml').exists())
            entry['version'] = self.version
            entry['source']['path'] = str(self.base / 'foreign')
            with self.assertRaisesRegex(ValueError, '来源'):
                manager.install(self.root)
            self.assertFalse((self.base / 'codex/agents/dev_product.toml').exists())
            entry['source']['path'] = str(self.root / '.dev-flow/plugin-source')
            manager.install(self.root)
            for version in (self.other_version, None):
                entry['version'] = version
                with self.assertRaisesRegex(ValueError, '版本'):
                    manager.check(self.root)

    def test_missing_prompt_and_routed_skill_are_rejected(self):
        (self.root / 'agents/prompts/product.md').unlink()
        with self.assertRaisesRegex(ValueError, '缺少包内文件'):
            manager.build(self.root)
        source = Path(__file__).resolve().parents[1]
        shutil.copy2(source / 'agents/prompts/product.md', self.root / 'agents/prompts/product.md')
        manifest = self.root / 'capabilities.json'
        value = json.loads(manifest.read_text())
        value['roles']['product']['skills'] = ['missing-skill']
        manifest.write_text(json.dumps(value))
        with self.assertRaisesRegex(ValueError, '路由无效'):
            manager.build(self.root)

    def test_missing_linked_resource_and_undeclared_skill_are_rejected(self):
        path = self.root / 'agents/prompts/product.md'
        path.write_text(path.read_text() + '\n[缺项](../references/product/missing.md)\n')
        with self.assertRaisesRegex(ValueError, '引用缺失'):
            manager.build(self.root)
        source = Path(__file__).resolve().parents[1]
        shutil.copy2(source / 'agents/prompts/product.md', path)
        extra = self.root / 'skills/dev-product/SKILL.md'
        extra.parent.mkdir(exist_ok=True)
        extra.write_text('---\nname: dev-product\ndescription: retired role\n---\n')
        with self.assertRaisesRegex(ValueError, '未声明'):
            manager.build(self.root)

    def test_missing_referenced_template_and_tool_are_rejected(self):
        template = self.root / 'agents/assets/engineering/engineering-handoff.md'
        template.unlink()
        with self.assertRaisesRegex(ValueError, '缺少包内文件|引用缺失'):
            manager.build(self.root)
        source = Path(__file__).resolve().parents[1]
        shutil.copy2(source / 'agents/assets/engineering/engineering-handoff.md', template)
        tool = self.root / 'skills/dev-flow/scripts/check_iteration.py'
        tool.unlink()
        with self.assertRaisesRegex(ValueError, '缺少包内文件'):
            manager.build(self.root)

    def test_generated_host_links_match_source(self):
        import importlib
        generator = importlib.import_module('sync_host_agents')
        expected = generator.expected_files(self.root)
        for relative in ('agents/dev_product.toml', 'adapters/kimi/agents/dev-product.md'):
            self.assertEqual((self.root / relative).read_text(), expected[relative])
        self.assertIn('agents/references', expected['adapters/kimi/agents/dev-product.md'])

    def test_broken_professional_template_link_is_rejected(self):
        template = self.root / 'agents/assets/engineering/engineering-review.md'
        template.write_text(template.read_text() + '\n[旧路径](../../../skills/dev-engineering/assets/design.md)\n')
        with self.assertRaisesRegex(ValueError, '引用缺失'):
            manager.build(self.root)

    def test_broken_operational_asset_link_is_rejected(self):
        template = self.root / 'skills/document-management/assets/templates/iteration-index.md'
        template.write_text(template.read_text() + '\n[错误进度](MissingProgress.md)\n')
        with self.assertRaisesRegex(ValueError, '引用缺失'):
            manager.build(self.root)

    def test_unlinked_professional_template_is_required(self):
        (self.root / 'agents/assets/architecture/templates/architecture-review.md').unlink()
        with self.assertRaisesRegex(ValueError, '缺少包内文件'):
            manager.build(self.root)

    def test_installed_lookup_does_not_scan_other_marketplaces(self):
        with patch.object(manager, 'cli', return_value={'installed': []}) as command:
            self.assertIsNone(manager.installed_entry())
        command.assert_called_once_with(['plugin', 'list', '--marketplace', manager.MARKETPLACE])


if __name__ == '__main__':
    unittest.main()
