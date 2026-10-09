"""宿主入口漂移、打包完整性及原 Codex 生命周期的隔离回归。"""
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import sync_host_agents as sync
import manage_plugin as manager


class HostAdapters(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory(prefix="dev-flow-host-check-")
        cls.root = Path(cls.temp.name) / "repo"
        shutil.copytree(ROOT, cls.root, ignore=shutil.ignore_patterns(".git", ".dev-flow", "node_modules", "dist", "__pycache__"))
        subprocess.run(["git", "init", "-q", str(cls.root)], check=True)
        subprocess.run(["git", "add", "."], cwd=cls.root, check=True)
        subprocess.run(["git", "-c", "user.name=Adapter Test", "-c", "user.email=adapter@example.invalid", "commit", "-qm", "fixture"], cwd=cls.root, check=True)

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def test_shared_skill_description_drift_is_rejected(self):
        skill = self.root / "skills/dev-product/SKILL.md"
        original = skill.read_text()
        try:
            skill.write_text(original.replace("description: ", "description: 更新职责：", 1))
            with self.assertRaisesRegex(ValueError, "未同步"):
                sync.check(self.root)
            with self.assertRaisesRegex(ValueError, "未同步"):
                manager.build(self.root)
        finally:
            skill.write_text(original)

    def test_generated_agent_drift_is_rejected(self):
        agent = self.root / "adapters/kimi/agents/dev-architecture.md"
        original = agent.read_text()
        try:
            agent.write_text(original + "手工追加的专业规则\n")
            with self.assertRaisesRegex(ValueError, "未同步"):
                sync.check(self.root)
        finally:
            agent.write_text(original)

    def test_unexpected_native_agent_is_rejected(self):
        agent = self.root / "adapters/kimi/agents/unmanaged.md"
        try:
            agent.write_text("---\nname: unmanaged\ndescription: unmanaged\n---\n")
            with self.assertRaisesRegex(ValueError, "未同步"):
                sync.check(self.root)
        finally:
            agent.unlink()

    def test_manifest_version_drift_is_rejected(self):
        manifest = self.root / "kimi.plugin.json"
        original = manifest.read_text()
        try:
            changed = json.loads(original); changed["version"] = "99.0.0"
            manifest.write_text(json.dumps(changed))
            with self.assertRaisesRegex(ValueError, "未同步"):
                sync.check(self.root)
        finally:
            manifest.write_text(original)

    def test_build_contains_native_agents_and_rejects_tampering(self):
        built = manager.build(self.root)
        package = Path(built["build_root"])
        self.assertEqual(len(manager.validate_bundle(package)), 7)
        self.assertEqual(len(list((package / "adapters/kimi/agents").glob("*.md"))), 6)
        manifest = json.loads((package / "kimi.plugin.json").read_text())
        self.assertEqual(manifest["agents"], "./adapters/kimi/agents/")
        self.assertFalse((package / ".dev-flow").exists())
        target = package / "adapters/kimi/agents/dev-product.md"
        original = target.read_text()
        try:
            target.write_text(original + "tampered\n")
            with self.assertRaisesRegex(ValueError, "内容不匹配"):
                manager.validate_bundle(package)
        finally:
            target.write_text(original)

    def test_codex_lifecycle_preserves_user_files_and_foreign_sources(self):
        # fake 只模拟 Codex CLI 边界；不把此用例登记为真实宿主安装。
        user = Path(self.temp.name) / "user"
        user.mkdir(exist_ok=True)
        config = user / "config.toml"; config.write_text("user_settings = true\n")
        instructions = user / "AGENTS.md"; instructions.write_text("用户原有指引\n")
        state = {"installed": [], "marketplaces": []}
        original_cli = manager.cli
        cache = Path(self.temp.name) / "cache"
        def fake_cli(args):
            if args == ["plugin", "marketplace", "list"]:
                return {"marketplaces": state["marketplaces"]}
            if args[:3] == ["plugin", "marketplace", "add"]:
                state["marketplaces"] = [{"name": manager.MARKETPLACE, "root": args[3]}]; return {}
            if args == ["plugin", "list"]:
                return {"installed": state["installed"]}
            if args[:2] == ["plugin", "add"]:
                if cache.exists(): shutil.rmtree(cache)
                shutil.copytree(self.root / ".dev-flow/plugin-source", cache)
                state["installed"] = [{"pluginId": manager.PLUGIN_ID, "enabled": True,
                    "source": {"path": str(self.root / ".dev-flow/plugin-source")}}]
                return {"installedPath": str(cache)}
            if args[:2] == ["plugin", "remove"]:
                state["installed"] = []; return {}
            if args[:3] == ["plugin", "marketplace", "remove"]:
                state["marketplaces"] = []; return {}
            raise AssertionError(args)
        manager.cli = fake_cli
        try:
            self.assertEqual(manager.install(self.root)["skills"], 7)
            self.assertTrue(manager.check(self.root)["source_matches_cache"])
            state["installed"][0]["source"]["path"] = str(user / "foreign")
            with self.assertRaisesRegex(ValueError, "其他来源"):
                manager.remove(self.root)
            self.assertTrue(state["installed"])
            state["installed"][0]["source"]["path"] = str(self.root / ".dev-flow/plugin-source")
            self.assertTrue(manager.remove(self.root)["source_and_project_assets_preserved"])
            self.assertEqual(config.read_text(), "user_settings = true\n")
            self.assertEqual(instructions.read_text(), "用户原有指引\n")
        finally:
            manager.cli = original_cli


if __name__ == "__main__":
    unittest.main()
