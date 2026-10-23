#!/usr/bin/env python3
"""从 Git 管理的源码构建、安装、检查和解除本地 Dev Flow 插件。"""

import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

from sync_host_agents import check as check_host_agents, load_capabilities
from native_agents import NativeAgents


PLUGIN_ID = "dev-flow@dev-flow-local"
MARKETPLACE = "dev-flow-local"
EXCLUDED = {".git", ".dev-flow", "node_modules", "dist", "__pycache__"}


def run(argv, cwd):
    process = subprocess.run(argv, cwd=cwd, capture_output=True, text=True)
    if process.returncode:
        raise ValueError("命令失败：" + " ".join(map(str, argv)) + "\n" + process.stderr.strip())
    return process.stdout


def cli(arguments):
    # 不在开发仓库内发现同名 repo marketplace，使用已配置的用户级来源。
    return json.loads(run(["codex"] + arguments + ["--json"], Path.home()))


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def atomic_text(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    handle, temporary = tempfile.mkstemp(dir=path.parent, prefix=".dev-flow-")
    try:
        with os.fdopen(handle, "w", encoding="utf-8") as stream:
            stream.write(value)
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def validate_bundle(root):
    root = Path(root)
    inventory = json.loads((root / "package-files.json").read_text())
    if inventory["owner"] != "dev-flow":
        raise ValueError("安装包不属于 Dev Flow")
    for relative, expected in inventory["files"].items():
        if Path(relative).is_absolute() or ".." in Path(relative).parts:
            raise ValueError("安装包路径越界：" + relative)
        candidate = root / relative
        file = candidate.resolve()
        if root.resolve() not in file.parents or candidate.is_symlink() or not file.is_file() or digest(file) != expected:
            raise ValueError("安装包路径或内容不匹配：" + relative)
    actual = {p.relative_to(root).as_posix() for p in root.rglob("*") if p.is_file() and p.name != "package-files.json"}
    if actual != set(inventory["files"]):
        raise ValueError("安装包文件与指纹清单不一致")
    check_host_agents(root)
    return load_capabilities(root)["skills"]


def tracked(root):
    raw = subprocess.check_output(["git", "ls-files", "-z"], cwd=root)
    files = []
    for entry in raw.decode("utf-8").split("\0"):
        if not entry:
            continue
        path = Path(entry)
        if EXCLUDED.intersection(path.parts):
            continue
        if path.name.startswith(".env") and path.name not in {".env.example", ".env.sample"}:
            continue
        source = root / path
        if source.is_symlink():
            raise ValueError("打包只接受 Git 管理的实际文件，先明确链接内容：" + entry)
        if source.is_file():
            files.append(entry)
    for required in ("plugin.json", ".codex-plugin/plugin.json", ".agents/plugins/marketplace.json",
                     "kimi.plugin.json", "capabilities.json", "scripts/sync_host_agents.py", "skills/dev-flow/SKILL.md"):
        if required not in files:
            raise ValueError("需要先将新插件文件纳入 Git：" + required)
    return files


def build(root):
    check_host_agents(root)
    files = tracked(root)
    build_root = root / ".dev-flow/plugin-source"
    build_root.parent.mkdir(parents=True, exist_ok=True)
    if build_root.exists():
        marker = build_root / "package-files.json"
        if build_root.is_symlink() or not marker.is_file() or json.loads(marker.read_text())["owner"] != "dev-flow":
            raise ValueError("构建目录不属于本工具，保留：" + str(build_root))
    temporary = Path(tempfile.mkdtemp(prefix="plugin-build-", dir=build_root.parent))
    try:
        hashes = {}
        for entry in files:
            target = temporary / entry
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(root / entry, target)
            hashes[entry] = digest(target)
        portable = json.loads((temporary / "plugin.json").read_text())
        compatibility = json.loads((temporary / ".codex-plugin/plugin.json").read_text())
        if any(portable[key] != compatibility[key] for key in ("name", "version", "description")):
            raise ValueError("便携清单与 Codex 兼容清单的身份不一致")
        catalog = json.loads((temporary / ".agents/plugins/marketplace.json").read_text())
        if catalog["name"] != MARKETPLACE or catalog["plugins"][0]["source"]["path"] != "./":
            raise ValueError("本地 marketplace 未指向干净包根目录")
        metadata = {"owner": "dev-flow", "schema": 1, "files": hashes,
                    "source_commit": run(["git", "rev-parse", "HEAD"], root).strip(),
                    "working_tree_changes": run(["git", "status", "--porcelain"], root).splitlines()}
        atomic_text(temporary / "package-files.json", json.dumps(metadata, ensure_ascii=False, indent=2) + "\n")
        validate_bundle(temporary)
        if build_root.exists():
            shutil.rmtree(build_root)
        temporary.rename(build_root)
    finally:
        if temporary.exists():
            shutil.rmtree(temporary)
    return {"build_root": str(build_root), "files": len(files),
            "bytes": sum((build_root / entry).stat().st_size for entry in files),
            "package_hash": digest(build_root / "package-files.json")}


def installed_entry():
    return next((p for p in cli(["plugin", "list", "--marketplace", MARKETPLACE])["installed"] if p["pluginId"] == PLUGIN_ID), None)


def verify_active_cache(root, entry, cached):
    """The local install record alone cannot prove which version is active."""
    version = json.loads((cached / "plugin.json").read_text())["version"]
    if not entry.get("version") or entry["version"] != version:
        raise ValueError("实际启用插件版本与安装缓存不一致，请运行 install")
    source = entry.get("source", {}).get("path")
    if not source or Path(source).resolve() != (root / ".dev-flow/plugin-source").resolve():
        raise ValueError("实际启用插件来源与当前仓库不一致，保留角色配置")


def install(root):
    with NativeAgents(root).locked() as agents:
        _, snapshot = agents.preflight()
        return install_locked(root, agents, snapshot)


def install_locked(root, agents, snapshot):
    build_root = root / ".dev-flow/plugin-source"
    existing = next((m for m in cli(["plugin", "marketplace", "list"])["marketplaces"] if m["name"] == MARKETPLACE), None)
    if existing and Path(existing["root"]).resolve() != build_root:
        raise ValueError("同名 marketplace 已指向其他目录：" + existing["root"])
    info = build(root)
    cli(["plugin", "marketplace", "add", str(build_root)])
    result = cli(["plugin", "add", PLUGIN_ID])
    cached = Path(result["installedPath"]).resolve()
    if digest(cached / "package-files.json") != info["package_hash"]:
        raise ValueError("安装缓存未刷新到当前源码；先检查 Codex 插件刷新结果")
    entry = installed_entry()
    if not entry or not entry["enabled"]:
        raise ValueError("插件尚未实际安装并启用")
    skills = validate_bundle(cached)
    verify_active_cache(root, entry, cached)
    registered = agents.register(cached, snapshot, root / ".dev-flow/plugin-install.json",
                                {"plugin_id": PLUGIN_ID, "plugin_root": str(cached)})
    return {"plugin_id": PLUGIN_ID, "build": info, "skills": len(skills), "native_agents": registered}


def check(root):
    with NativeAgents(root).locked() as agents:
        return check_locked(root, agents)


def check_locked(root, agents):
    entry = installed_entry()
    if not entry or not entry["enabled"]:
        raise ValueError("当前用户没有启用 " + PLUGIN_ID)
    if Path(entry["source"]["path"]).resolve() != (root / ".dev-flow/plugin-source").resolve():
        raise ValueError("插件来源已改变，不能用本仓库记录核验")
    record = json.loads((root / ".dev-flow/plugin-install.json").read_text())
    if record["plugin_id"] != PLUGIN_ID:
        raise ValueError("安装记录不属于本插件")
    cached = Path(record["plugin_root"])
    skills = validate_bundle(cached)
    verify_active_cache(root, entry, cached)
    inventory = json.loads((cached / "package-files.json").read_text())
    source_files = tracked(root)
    if set(source_files) != set(inventory["files"]) or any(
            digest(root / name) != expected for name, expected in inventory["files"].items()):
        raise ValueError("源码已变化，运行 install 重建并刷新插件")
    registered = agents.check(cached)
    return {"plugin_id": PLUGIN_ID, "enabled": True, "source_matches_cache": True,
            "skills": len(skills), "native_agents": registered}


def remove(root):
    with NativeAgents(root).locked() as agents:
        _, snapshot = agents.preflight(removing=True)
        return remove_locked(root, agents, snapshot)


def remove_locked(root, agents, snapshot):
    entry = installed_entry()
    if entry and Path(entry["source"]["path"]).resolve() != (root / ".dev-flow/plugin-source").resolve():
        raise ValueError("同名插件已经换成其他来源，保留并报告")
    if entry:
        cli(["plugin", "remove", PLUGIN_ID])
    existing = next((m for m in cli(["plugin", "marketplace", "list"])["marketplaces"] if m["name"] == MARKETPLACE), None)
    if existing and Path(existing["root"]).resolve() == root / ".dev-flow/plugin-source":
        cli(["plugin", "marketplace", "remove", MARKETPLACE])
    agents.remove(snapshot, root / ".dev-flow/plugin-install.json")
    return {"plugin_id": PLUGIN_ID, "source_and_project_assets_preserved": True}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("build", "install", "check", "remove"))
    root = Path(__file__).resolve().parent.parent
    args = parser.parse_args()
    print(json.dumps({"build": build, "install": install, "check": check, "remove": remove}[args.command](root), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, KeyError, subprocess.SubprocessError) as exc:
        print(str(exc), file=sys.stderr)
        sys.exit(1)
