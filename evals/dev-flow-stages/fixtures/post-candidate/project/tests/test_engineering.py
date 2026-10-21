"""候选形成时的研发局部自测；正式验收另行维护。"""

import contextlib
import io
from pathlib import Path
import tempfile
import unittest

from order_notes.cli import main


class EngineeringSmokeTest(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.store = Path(self.directory.name) / "notes.json"

    def run_cli(self, *arguments):
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = main(["--store", str(self.store), *arguments])
        return code, out.getvalue(), err.getvalue()

    def test_save_and_read(self):
        self.assertEqual(self.run_cli("save", "--order", "A-1", "--note", "门口放置", "--role", "editor")[0], 0)
        self.assertEqual(self.run_cli("show", "--order", "A-1"), (0, "门口放置\n", ""))

    def test_viewer_is_rejected_without_writing(self):
        self.assertEqual(self.run_cli("save", "--order", "A-1", "--note", "旧", "--role", "editor")[0], 0)
        before = self.store.read_bytes()
        self.assertEqual(self.run_cli("save", "--order", "A-1", "--note", "新", "--role", "viewer")[0], 1)
        self.assertEqual(self.store.read_bytes(), before)

    def test_failed_write_keeps_original_and_retry_succeeds(self):
        self.assertEqual(self.run_cli("save", "--order", "A-1", "--note", "旧", "--role", "editor")[0], 0)
        before = self.store.read_bytes()
        self.assertEqual(self.run_cli("save", "--order", "A-1", "--note", "新", "--role", "editor", "--fail-before-commit")[0], 1)
        self.assertEqual(self.store.read_bytes(), before)
        self.assertEqual(self.run_cli("save", "--order", "A-1", "--note", "新", "--role", "editor")[0], 0)
        self.assertEqual(self.run_cli("show", "--order", "A-1"), (0, "新\n", ""))


if __name__ == "__main__":
    unittest.main()
