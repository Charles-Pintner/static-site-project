import unittest
from markdown_blocks import markdown_to_blocks
from markdown_blocks import BlockType, block_to_block_type
from markdown_blocks import markdown_to_html_node
class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_excessive_newlines(self):
        md = """

# Heading


Paragraph text



- List item 1
- List item 2


"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "# Heading",
                "Paragraph text",
                "- List item 1\n- List item 2",
            ],
        )

    def test_single_block(self):
        md = "Just a single paragraph with no breaks."
        self.assertEqual(
            markdown_to_blocks(md),
            ["Just a single paragraph with no breaks."]
        )


if __name__ == "__main__":
    unittest.main()

class TestBlockToBlockType(unittest.TestCase):

    def test_heading_blocks(self):
        self.assertEqual(
            block_to_block_type("# Heading"),
            BlockType.HEADING
        )
        self.assertEqual(
            block_to_block_type("###### Heading 6"),
            BlockType.HEADING
        )

    def test_code_block(self):
        block = "```\nprint('hello')\n```"
        self.assertEqual(
            block_to_block_type(block),
            BlockType.CODE
        )

    def test_quote_block(self):
        block = "> Quote line 1\n> Quote line 2"
        self.assertEqual(
            block_to_block_type(block),
            BlockType.QUOTE
        )

    def test_unordered_list(self):
        block = "- Item one\n- Item two\n- Item three"
        self.assertEqual(
            block_to_block_type(block),
            BlockType.UNORDERED_LIST
        )

    def test_ordered_list(self):
        block = "1. First\n2. Second\n3. Third"
        self.assertEqual(
            block_to_block_type(block),
            BlockType.ORDERED_LIST
        )

    def test_invalid_ordered_list(self):
        block = "1. First\n3. Third"
        self.assertEqual(
            block_to_block_type(block),
            BlockType.PARAGRAPH
        )

    def test_paragraph(self):
        block = "This is a normal paragraph of text."
        self.assertEqual(
            block_to_block_type(block),
            BlockType.PARAGRAPH
        )

    def test_mixed_block_is_paragraph(self):
        block = "- Item one\nNot a list item"
        self.assertEqual(
            block_to_block_type(block),
            BlockType.PARAGRAPH
        )


if __name__ == "__main__":
    unittest.main()

class TestMarkdownToHTMLNode(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph text in a p tag here

This is another paragraph with _italic_ text and `code` here
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p>"
            "<p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """"""
