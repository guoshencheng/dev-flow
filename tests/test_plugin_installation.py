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
        for name in ['plugin.json', '.codex-plugin/plugin.json', '.agents/plugins/marketplace.json']:
            target = self.root / name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source / name, target)
        for skill in (source / 'skills').glob('*/SKILL.md'):
            target = self.root / 'skills' / skill.parent.name / 'SKILL.md'
            target.parent.mkdir(parents=True)
            shutil.copy2(skill, target)
        subprocess.run(['git', 'init', '-q', str(self.root)], check=True)
        subprocess.run(['git', 'add', '.'], cwd=self.root, check=True)
        subprocess.run(['git', '-c', 'user.name=Test', '-c', 'user.email=test@example.com', 'commit', '-qm', 'fixture'], cwd=self.root, check=True)

    def tearDown(self):
        self.temp.cleanup()

    def test_package_without_setup_and_rebuild(self):
        result = manager.build(self.root)
        bundle = Path(result['build_root'])
        self.assertEqual(len(manager.validate_bundle(bundle)), 7)
        self.assertFalse((bundle / 'skills/dev-flow-setup').exists())
        self.assertFalse((bundle / 'scripts/setup_plugin.py').exists())
        original = result['package_hash']
        (self.root / 'skills/dev-flow/SKILL.md').write_text('changed')
        self.assertNotEqual(manager.build(self.root)['package_hash'], original)

    def test_tampered_cache_is_rejected(self):
        bundle = Path(manager.build(self.root)['build_root'])
        (bundle / 'skills/dev-flow/SKILL.md').write_text('tampered')
        with self.assertRaises(ValueError):
            manager.validate_bundle(bundle)

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
            if args == ['plugin', 'list']:
                return {'installed': present}
            if args[:2] == ['plugin', 'remove']:
                present.clear()
            return {}
        with patch.object(manager, 'cli', side_effect=fake_cli), patch.object(Path, 'home', return_value=personal):
            self.assertEqual(manager.install(self.root)['skills'], 7)
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


if __name__ == '__main__':
    unittest.main()
