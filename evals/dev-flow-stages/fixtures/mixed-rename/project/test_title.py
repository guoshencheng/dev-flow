import unittest
import app
class Title(unittest.TestCase):
    def test_title(self): self.assertEqual(app.TITLE, "运动结算")
    def test_platform(self): self.assertEqual(app.PLATFORM, "Mac")
