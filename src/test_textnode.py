import unittest

from textnode import TextNode, TextType
from main import text_node_to_html_node

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq_text(self):
        node = TextNode("Hello", TextType.BOLD)
        node2 = TextNode("Goodbye", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_not_eq_text_type(self):
        node = TextNode("Same text", TextType.BOLD)
        node2 = TextNode("Same text", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_eq_with_url(self):
        node = TextNode("Click me", TextType.LINK, "https://example.com")
        node2 = TextNode("Click me", TextType.LINK, "https://example.com")
        self.assertEqual(node, node2)

    def test_not_eq_url(self):
        node = TextNode("Click me", TextType.LINK, "https://a.com")
        node2 = TextNode("Click me", TextType.LINK, "https://b.com")
        self.assertNotEqual(node, node2)

    def test_default_url_is_none(self):
        node = TextNode("Text", TextType.TEXT)
        node2 = TextNode("Text", TextType.TEXT, None)
        self.assertEqual(node, node2)


if __name__ == "__main__":
    unittest.main()


class TestTextNodeConversion(unittest.TestCase):

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html = text_node_to_html_node(node)
        self.assertEqual(html.tag, None)
        self.assertEqual(html.value, "This is a text node")

    def test_bold(self):
        node = TextNode("bold text", TextType.BOLD)
        html = text_node_to_html_node(node)
        self.assertEqual(html.tag, "b")
        self.assertEqual(html.value, "bold text")

    def test_italic(self):
        node = TextNode("italic text", TextType.ITALIC)
        html = text_node_to_html_node(node)
        self.assertEqual(html.tag, "i")
        self.assertEqual(html.value, "italic text")

    def test_code(self):
        node = TextNode("x = 1", TextType.CODE)
        html = text_node_to_html_node(node)
        self.assertEqual(html.tag, "code")
        self.assertEqual(html.value, "x = 1")

    def test_link(self):
        node = TextNode("OpenAI", TextType.LINK, url="https://openai.com")
        html = text_node_to_html_node(node)
        self.assertEqual(html.tag, "a")
        self.assertEqual(html.value, "OpenAI")
        self.assertEqual(html.props, {"href": "https://openai.com"})

    def test_image(self):
        node = TextNode("An image", TextType.IMAGE, url="image.png")
        html = text_node_to_html_node(node)
        self.assertEqual(html.tag, "img")
        self.assertEqual(html.value, "")
        self.assertEqual(html.props, {"src": "image.png", "alt": "An image"})

    def test_invalid_type(self):
        class FakeType: pass
        node = TextNode("bad", FakeType())
        with self.assertRaises(Exception):
            text_node_to_html_node(node)
