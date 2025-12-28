import unittest
from htmlnode import HTMLNode
from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_raw_text(self):
        node = LeafNode(None, "Just text")
        self.assertEqual(node.to_html(), "Just text")

    def test_leaf_to_html_link(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(
            node.to_html(),
            '<a href="https://www.google.com">Click me!</a>'
        )

    def test_leaf_requires_value(self):
        with self.assertRaises(ValueError):
            LeafNode("p", None)

    def test_leaf_does_not_allow_children(self):
        node = LeafNode("span", "text")
        # The constructor always forces children = []
        self.assertEqual(node.children, [])

    def test_leaf_with_multiple_props(self):
        node = LeafNode("img", "image", {"src": "cat.jpg", "alt": "cat"})
        self.assertEqual(
            node.to_html(),
            '<img src="cat.jpg" alt="cat">image</img>'
        )


if __name__ == "__main__":
    unittest.main()
