"""隔离验证插件打包、缓存核验及用户配置不变。"""
import json
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
        self.root = self.base / 'repo'
        self.root.mkdir()
        source = Path(__file__).resolve().parents[1]
        # 夹具与实际打包使用相同源码边界，排除本机旧目录、依赖和构建物。
        for relative in manager.tracked(source):
            target = self.root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source / relative, target)
        subprocess.run(['git', 'init', '-q', str(self.root)], check=True)
        subprocess.run(['git', 'add', '.'], cwd=self.root, check=True)
        subprocess.run(['git', '-c', 'user.name=Test', '-c', 'user.email=test@example.com', 'commit', '-qm', 'fixture'], cwd=self.root, check=True)

    def tearDown(self):
        self.temp.cleanup()

    def test_package_without_setup_and_rebuild(self):
        result = manager.build(self.root)
        bundle = Path(result['build_root'])
        self.assertEqual(len(manager.validate_bundle(bundle)), 16)
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
        (personal / 'agents').mkdir(parents=True)
        guide = personal / 'AGENTS.md'
        guide.write_text('已有流程指引')
        role = personal / 'agents/custom.toml'
        role.write_text('用户角色')
        cached = self.base / 'cache'
        entry = {'pluginId': manager.PLUGIN_ID, 'enabled': True,
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
            self.assertEqual(manager.install(self.root)['skills'], 16)
            self.assertTrue(manager.check(self.root)['source_matches_cache'])
            manager.remove(self.root)
        self.assertEqual(guide.read_text(), '已有流程指引')
        self.assertEqual(role.read_text(), '用户角色')
        self.assertEqual(set(personal.iterdir()), {personal / 'agents', guide})
        self.assertFalse((self.root / '.dev-flow/plugin-install.json').exists())

    def test_foreign_marketplace_stops_install(self):
        with patch.object(manager, 'cli', return_value={'marketplaces': [{'name': manager.MARKETPLACE, 'root': str(self.base / 'foreign')}]}):
            with self.assertRaises(ValueError):
                manager.install(self.root)
        self.assertFalse((self.root / '.dev-flow/plugin-source').exists())

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
