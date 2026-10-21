import unittest
from permissions import can_save

class Permissions(unittest.TestCase):
    def test_reader_cannot_save(self):
        self.assertFalse(can_save("reader"))
    def test_editor_can_save(self):
        self.assertTrue(can_save("editor"))

if __name__ == "__main__": unittest.main()
