"""用单个 JSON 文件保存订单备注的命令行入口。"""

import argparse
import json
import os
from pathlib import Path
import sys
import tempfile


class NoteError(Exception):
    pass


def read_store(path):
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise NoteError(f"无法读取备注文件：{exc}") from exc
    if not isinstance(data, dict) or any(
        not isinstance(key, str) or not isinstance(value, str)
        for key, value in data.items()
    ):
        raise NoteError("备注文件格式无效")
    return data


def write_store(path, data, fail_before_commit=False):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", dir=path.parent,
            prefix=f".{path.name}.", suffix=".tmp", delete=False,
        ) as handle:
            temporary = Path(handle.name)
            json.dump(data, handle, ensure_ascii=False, sort_keys=True)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        if fail_before_commit:
            raise OSError("模拟提交前写入失败")
        os.replace(temporary, path)
    except OSError as exc:
        raise NoteError(f"保存失败，原备注文件未改动：{exc}") from exc
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def main(argv=None):
    parser = argparse.ArgumentParser(description="保存和读取订单备注")
    parser.add_argument("--store", type=Path, required=True, help="备注 JSON 文件路径")
    commands = parser.add_subparsers(dest="command", required=True)
    save = commands.add_parser("save", help="保存单个订单备注")
    save.add_argument("--order", required=True)
    save.add_argument("--note", required=True)
    save.add_argument("--role", choices=("editor", "viewer"), required=True)
    save.add_argument("--fail-before-commit", action="store_true", help="模拟提交前写入失败")
    show = commands.add_parser("show", help="读取单个订单备注")
    show.add_argument("--order", required=True)
    args = parser.parse_args(argv)

    try:
        if not args.order.strip():
            raise NoteError("订单编号不能为空")
        if args.command == "save":
            if args.role == "viewer":
                raise NoteError("只读用户不能保存备注")
            if not args.note.strip() or len(args.note) > 120:
                raise NoteError("备注须为 1 至 120 个字符，且不能全为空白")
            data = read_store(args.store)
            data[args.order] = args.note
            write_store(args.store, data, args.fail_before_commit)
            print(f"已保存订单 {args.order} 的备注")
        else:
            data = read_store(args.store)
            if args.order not in data:
                raise NoteError(f"订单 {args.order} 没有备注")
            print(data[args.order])
    except NoteError as exc:
        print(f"错误：{exc}", file=sys.stderr)
        return 1
    return 0
