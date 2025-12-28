import unittest

from textnode import TextNode, TextType
from splitter import split_nodes_image, split_nodes_link


class TestSplitNodesImage(unittest.TestCase):
    def test_multiple_adjacent_images(self):
        node = TextNode("![a](1)![b](2)![c](3)", TextType.TEXT)
        new = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("a", TextType.IMAGE, "1"),
                TextNode("b", TextType.IMAGE, "2"),
                TextNode("c", TextType.IMAGE, "3"),
            ],
            new,
        )


class TestSplitNodesLink(unittest.TestCase):
    def test_multiple_adjacent_links(self):
        node = TextNode("[a](1)[b](2)[c](3)", TextType.TEXT)
        new = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("a", TextType.LINK, "1"),
                TextNode("b", TextType.LINK, "2"),
                TextNode("c", TextType.LINK, "3"),
            ],
            new,
        )


if __name__ == "__main__":
    unittest.main()
