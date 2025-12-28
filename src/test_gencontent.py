
import unittest
from gencontent import extract_title

class TestExtractTitle(unittest.TestCase):

    def test_simple_h1(self):
        md = "# Hello"
        self.assertEqual(extract_title(md), "Hello")

    def test_h1_with_whitespace(self):
        md = "#   Hello World   "
        self.assertEqual(extract_title(md), "Hello World")

    def test_h1_not_first_line(self):
        md = "Some text\n# Title\nMore text"
        self.assertEqual(extract_title(md), "Title")

    def test_no_h1_raises(self):
        md = "## Subtitle\nNo title here"
        with self.assertRaises(Exception):
            extract_title(md)

if __name__ == "__main__":
    unittest.main()
