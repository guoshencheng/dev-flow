#!/usr/bin/env python3
"""初始化或启动独立 HTML 交互原型；只使用 Python 标准库。"""

from __future__ import annotations

import argparse
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
import shutil
import shlex
import sys


ASSETS = Path(__file__).resolve().parent.parent / "assets" / "prototype"


def initialize(destination: Path, title: str):
    destination = destination.expanduser().resolve()
    if destination.exists():
        raise ValueError("目标已存在，请选择新的原型目录：" + str(destination))
    if not title.strip():
        raise ValueError("原型标题不能为空")
    shutil.copytree(ASSETS, destination)
    config = destination / "public" / "prototype.json"
    data = json.loads(config.read_text(encoding="utf-8"))
    data["title"] = title.strip()
    config.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("已创建：" + str(destination))
    print("可编辑 public/ 中的原型与 prototype.json，在 review.md 记录讨论和决定。")
    print("启动方式：" + shlex.join(["python3", str(Path(__file__).resolve()), "serve", str(destination)]))


class PrototypeHandler(SimpleHTTPRequestHandler):
    """仅发布指定 public 目录，禁止目录枚举和越界链接。"""

    def send_head(self):
        root = Path(self.directory).resolve()
        try:
            Path(self.translate_path(self.path)).resolve().relative_to(root)
        except ValueError:
            self.send_error(403, "Outside prototype public directory")
            return None
        return super().send_head()

    def list_directory(self, path):
        self.send_error(403, "Directory listing disabled")
        return None

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        super().end_headers()


def serve(destination: Path, port: int):
    root = destination.expanduser().resolve() / "public"
    if not (root / "index.html").is_file():
        raise ValueError("未找到 public/index.html，请先初始化原型")
    if not 0 <= port <= 65535:
        raise ValueError("端口必须在 0 至 65535 之间；0 表示自动分配")
    handler = partial(PrototypeHandler, directory=str(root))
    with ThreadingHTTPServer(("127.0.0.1", port), handler) as server:
        address = "http://127.0.0.1:" + str(server.server_address[1]) + "/"
        print("原型地址：" + address, flush=True)
        print("只发布：" + str(root), flush=True)
        print("停止：Ctrl+C。修改文件后刷新页面；反馈需要导出后保存到项目。", flush=True)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\n原型服务已停止", flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    init = commands.add_parser("init", help="在新目录复制原型脚手架")
    init.add_argument("directory", type=Path)
    init.add_argument("--title", default="产品与交互讨论")
    start = commands.add_parser("serve", help="仅在本机启动 public/ 静态服务")
    start.add_argument("directory", type=Path)
    start.add_argument("--port", type=int, default=8765)
    args = parser.parse_args()
    if args.command == "init":
        initialize(args.directory, args.title)
    else:
        serve(args.directory, args.port)


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(str(error), file=sys.stderr)
        sys.exit(1)
