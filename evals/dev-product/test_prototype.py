"""验证原型工具的创建边界与发布范围；浏览器交互另见运行记录。"""

import contextlib
from functools import partial
from http.server import ThreadingHTTPServer
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import threading
import unittest
from urllib.error import HTTPError
from urllib.request import urlopen


SCRIPT = Path(__file__).resolve().parents[2] / "skills/dev-product/scripts/prototype.py"
spec = importlib.util.spec_from_file_location("dev_product_prototype", SCRIPT)
prototype = importlib.util.module_from_spec(spec)
spec.loader.exec_module(prototype)


class PrototypeTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.project = self.root / "含空格的 prototype"
        with contextlib.redirect_stdout(io.StringIO()):
            prototype.initialize(self.project, "预约讨论 <候选>")

    def tearDown(self):
        self.temp.cleanup()

    def test_initialization_preserves_metadata_and_rejects_overwrite(self):
        config = self.project / "public/prototype.json"
        self.assertEqual(json.loads(config.read_text())["title"], "预约讨论 <候选>")
        before = config.read_bytes()
        with self.assertRaises(ValueError):
            prototype.initialize(self.project, "不应覆盖")
        self.assertEqual(before, config.read_bytes())
        self.assertTrue((self.project / "review.md").is_file())

    def test_blank_title_creates_no_output(self):
        target = self.root / "invalid"
        with self.assertRaises(ValueError):
            prototype.initialize(target, "   ")
        self.assertFalse(target.exists())

    def test_server_publishes_only_public_and_rejects_escape(self):
        public = self.project / "public"
        (public / "unlisted").mkdir()
        outside = self.root / "private-test.txt"
        outside.write_text("仅用于验证的私有测试内容")
        (public / "escape.txt").symlink_to(outside)
        (public / "escaped-directory").symlink_to(self.root, target_is_directory=True)
        server = ThreadingHTTPServer(("127.0.0.1", 0), partial(prototype.PrototypeHandler, directory=str(public)))
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        base = "http://127.0.0.1:" + str(server.server_address[1])
        try:
            with urlopen(base + "/") as response:
                self.assertEqual(response.status, 200)
                self.assertEqual(response.headers["Cache-Control"], "no-store")
                self.assertIn("讨论场景".encode(), response.read())
            for relative, expected in (("/review.md", 404), ("/unlisted/", 403), ("/escape.txt", 403), ("/escaped-directory/private-test.txt", 403)):
                with self.subTest(path=relative):
                    with self.assertRaises(HTTPError) as result:
                        urlopen(base + relative)
                    self.assertEqual(result.exception.code, expected)
        finally:
            server.shutdown()
            server.server_close()
            thread.join(timeout=2)


if __name__ == "__main__":
    unittest.main()
