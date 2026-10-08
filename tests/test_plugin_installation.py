"""临时文件系统上的迁移、更新、冲突和解除验证。"""
import argparse
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import setup_plugin


class PluginSetupTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="dev-flow-plugin-test-")
        self.base = Path(self.temp.name)
        self.repo = Path(__file__).resolve().parents[1]
        self.root = self.bundle(self.base / "plugin with space")
        self.codex, self.skills = self.base / "codex", self.base / "skills"
        self.codex.mkdir()
        (self.codex / "AGENTS.md").write_text("既有中文规则\n", encoding="utf-8")
        self.args = argparse.Namespace(plugin_root=self.root, legacy_root=None,
                                       codex_dir=self.codex, skills_dir=self.skills)

    def tearDown(self):
        self.temp.cleanup()

    def bundle(self, target):
        target.mkdir()
        shutil.copy2(self.repo / "plugin.json", target / "plugin.json")
        shutil.copytree(self.repo / "agents", target / "agents")
        for source in (self.repo / "skills").glob("*/SKILL.md"):
            folder = target / "skills" / source.parent.name
            folder.mkdir(parents=True)
            shutil.copy2(source, folder / "SKILL.md")
        return target

    def state(self):
        return setup_plugin.state_at(self.codex / "dev-flow/plugin/state.json")

    def test_install_and_repeat(self):
        result = setup_plugin.apply(self.args)
        self.assertEqual((result["roles"], result["skills"]), (6, 8))
        before = list((self.codex / "backups/dev-flow").iterdir())
        self.assertEqual(setup_plugin.apply(self.args), result)
        self.assertEqual(list((self.codex / "backups/dev-flow").iterdir()), before)
        text = (self.codex / "AGENTS.md").read_text()
        self.assertTrue(text.startswith("既有中文规则\n"))
        self.assertEqual(text.count(setup_plugin.BEGIN), 1)

    def test_migrate_only_our_links(self):
        legacy = self.bundle(self.base / "legacy")
        self.args.legacy_root = legacy
        self.skills.mkdir()
        (self.skills / "another-skill").mkdir()
        for name in setup_plugin.inputs(legacy)[2]:
            (self.skills / name).symlink_to(legacy / "skills" / name)
        (self.codex / "agents").mkdir()
        for source in (legacy / "agents").glob("*.toml"):
            (self.codex / "agents" / source.name).symlink_to(source)
        setup_plugin.apply(self.args)
        self.assertTrue((self.skills / "another-skill").is_dir())
        self.assertFalse((self.skills / "dev-flow").is_symlink())
        text = (self.codex / "agents/dev_product.toml").read_text()
        self.assertIn(str(self.root / "skills/dev-product/SKILL.md"), text)
        self.assertNotIn("~/.agents/skills/", text)

    def test_foreign_role_rejected_before_writing(self):
        (self.codex / "agents").mkdir()
        target = self.codex / "agents/dev_product.toml"
        target.write_text("其他来源")
        with self.assertRaisesRegex(ValueError, "其他来源占用"):
            setup_plugin.apply(self.args)
        self.assertEqual(target.read_text(), "其他来源")
        self.assertFalse((self.codex / "backups").exists())
        self.assertIsNone(self.state())

    def test_foreign_skill_rejected_before_writing(self):
        (self.skills / "dev-flow").mkdir(parents=True)
        with self.assertRaisesRegex(ValueError, "其他来源"):
            setup_plugin.apply(self.args)
        self.assertEqual((self.codex / "AGENTS.md").read_text(), "既有中文规则\n")

    def test_update_changes_role_paths(self):
        setup_plugin.apply(self.args)
        newer = self.bundle(self.base / "new plugin")
        manifest = json.loads((newer / "plugin.json").read_text())
        manifest["version"] = "0.1.1"
        (newer / "plugin.json").write_text(json.dumps(manifest))
        self.args.plugin_root = newer
        self.assertEqual(setup_plugin.apply(self.args)["version"], "0.1.1")
        self.assertIn(str(newer / "skills/dev-product/SKILL.md"),
                      (self.codex / "agents/dev_product.toml").read_text())

    def test_modified_role_is_preserved(self):
        setup_plugin.apply(self.args)
        target = self.codex / "agents/dev_product.toml"
        target.write_text(target.read_text() + "\n# 用户修改\n")
        with self.assertRaisesRegex(ValueError, "未纳入的修改"):
            setup_plugin.apply(self.args)
        self.assertTrue(target.read_text().endswith("# 用户修改\n"))

    def test_modified_guidance_is_preserved(self):
        setup_plugin.apply(self.args)
        target = self.codex / "AGENTS.md"
        value = target.read_text().replace("按用户要求裁剪流程", "本次调整规则")
        target.write_text(value)
        with self.assertRaisesRegex(ValueError, "区块已修改"):
            setup_plugin.apply(self.args)
        self.assertEqual(target.read_text(), value)

    def test_override_and_malformed_block_rejected(self):
        (self.codex / "AGENTS.override.md").write_text("覆盖入口")
        with self.assertRaisesRegex(ValueError, "override"):
            setup_plugin.apply(self.args)
        (self.codex / "AGENTS.override.md").unlink()
        (self.codex / "AGENTS.md").write_text(setup_plugin.BEGIN)
        with self.assertRaisesRegex(ValueError, "标记不完整"):
            setup_plugin.apply(self.args)

    def test_remove_preserves_reclaimed_entries(self):
        setup_plugin.apply(self.args)
        unrelated = self.codex / "agents/other.toml"
        unrelated.write_text("其他角色")
        target = self.codex / "agents/dev_product.toml"
        target.unlink()
        target.write_text("其他来源已接管")
        setup_plugin.remove(self.args)
        self.assertEqual(unrelated.read_text(), "其他角色")
        self.assertEqual(target.read_text(), "其他来源已接管")
        self.assertNotIn(setup_plugin.BEGIN, (self.codex / "AGENTS.md").read_text())
        self.assertIn("既有中文规则", (self.codex / "AGENTS.md").read_text())
        self.assertIsNone(self.state())
        self.assertFalse(setup_plugin.remove(self.args)["removed"])

    def test_cache_corruption_is_detected(self):
        (self.root / "package-files.json").write_text(json.dumps({"files": {"plugin.json": "wrong"}}))
        with self.assertRaisesRegex(ValueError, "指纹不符"):
            setup_plugin.apply(self.args)
        self.assertIsNone(self.state())

    def test_same_version_content_refresh_updates_fingerprint(self):
        inventory = self.root / "package-files.json"
        marker = {"files": {"plugin.json": setup_plugin.digest(self.root / "plugin.json")}, "revision": 1}
        inventory.write_text(json.dumps(marker))
        setup_plugin.apply(self.args)
        previous = self.state()["package_hash"]
        marker["revision"] = 2
        inventory.write_text(json.dumps(marker))
        setup_plugin.apply(self.args)
        self.assertNotEqual(previous, self.state()["package_hash"])
        self.assertEqual(self.state()["package_hash"], setup_plugin.digest(inventory))

    def test_legacy_mode_is_repeatable_and_rejects_plugin_mode(self):
        import subprocess
        command = [sys.executable, str(self.repo / "scripts/install_global.py"),
                   "--codex-dir", str(self.codex), "--skills-dir", str(self.skills)]
        self.assertEqual(subprocess.run(command, capture_output=True).returncode, 0)
        self.assertEqual(subprocess.run(command + ["--check"], capture_output=True).returncode, 0)
        self.args.legacy_root = self.repo
        setup_plugin.apply(self.args)
        failed = subprocess.run(command, capture_output=True, text=True)
        self.assertNotEqual(failed.returncode, 0)
        self.assertIn("Plugin 模式", failed.stderr)

    def test_failed_update_restores_previous_files_and_links(self):
        from unittest.mock import patch
        setup_plugin.apply(self.args)
        old_state = self.state()
        old_guidance = (self.codex / "AGENTS.md").read_bytes()
        old_role = (self.codex / "agents/dev_acceptance.toml").read_bytes()
        self.args.plugin_root = self.bundle(self.base / "candidate")
        original_write = setup_plugin.atomic_text
        def fail_on_state(path, value):
            if path.name == "state.json":
                raise OSError("注入写入失败")
            return original_write(path, value)
        with patch.object(setup_plugin, "atomic_text", side_effect=fail_on_state):
            with self.assertRaisesRegex(OSError, "注入写入失败"):
                setup_plugin.apply(self.args)
        self.assertEqual(self.state(), old_state)
        self.assertEqual((self.codex / "AGENTS.md").read_bytes(), old_guidance)
        self.assertEqual((self.codex / "agents/dev_acceptance.toml").read_bytes(), old_role)
        self.args.plugin_root = self.root
        self.assertTrue(setup_plugin.check(self.args)["initialized"])

    def test_rendered_toml_has_no_fixed_model(self):
        try:
            import tomllib
        except ImportError:
            self.skipTest("解析检查使用 Python 3.11+；安装脚本兼容 3.9+")
        setup_plugin.apply(self.args)
        for path in (self.codex / "agents").glob("dev_*.toml"):
            data = tomllib.loads(path.read_text())
            self.assertEqual(data["name"], path.stem)
            self.assertNotIn("model", data)
            self.assertNotIn("model_reasoning_effort", data)


if __name__ == "__main__":
    unittest.main()
