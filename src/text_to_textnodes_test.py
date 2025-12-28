import unittest
from textnode import TextNode, TextType
from converter import text_to_textnodes


class TestTextToTextNodes(unittest.TestCase):

    def test_full_example(self):
        text = (
            "This is **text** with an _italic_ word and a `code block` "
            "and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) "
            "and a [link](https://boot.dev)"
        )

        nodes = text_to_textnodes(text)

        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode(
                "obi wan image",
                TextType.IMAGE,
                "https://i.imgur.com/fJRm4Vk.jpeg",
            ),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]

        self.assertListEqual(nodes, expected)

    def test_plain_text(self):
        text = "hello world"
        nodes = text_to_textnodes(text)
        self.assertListEqual(nodes, [TextNode("hello world", TextType.TEXT)])

    def test_only_bold(self):
        text = "test **bold** text"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("test ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertListEqual(nodes, expected)

    def test_only_italic(self):
        text = "this is _cool_"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("this is ", TextType.TEXT),
            TextNode("cool", TextType.ITALIC),
        ]
        self.assertListEqual(nodes, expected)

    def test_only_code(self):
        text = "here is `code`"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("here is ", TextType.TEXT),
            TextNode("code", TextType.CODE),
        ]
        self.assertListEqual(nodes, expected)

    def test_link_and_image(self):
        text = "![img](url) and [link](url2)"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("img", TextType.IMAGE, "url"),
            TextNode(" and ", TextType.TEXT),
            TextNode("link", TextType.LINK, "url2"),
        ]
        self.assertListEqual(nodes, expected)


if __name__ == "__main__":
    unittest.main()
