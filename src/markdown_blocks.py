from enum import Enum
from htmlnode import ParentNode
import inline_markdown
from textnode import TextNode, TextType
from textnode import text_node_to_html_node

def markdown_to_blocks(markdown):
    """
    Split a raw Markdown document into block strings.

    - Blocks are separated by one or more blank lines.
    - Leading/trailing whitespace is stripped from each block.
    - Empty blocks are removed.
    """
    # Split on double newlines
    raw_blocks = markdown.split("\n\n")

    blocks = []
    for block in raw_blocks:
        stripped = block.strip()
        if stripped:
            blocks.append(stripped)

    return blocks

class BlockType(Enum):
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"
    PARAGRAPH = "paragraph"


def block_to_block_type(block: str) -> BlockType:
    lines = block.split("\n")

    # Code block: must start and end with ```
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE

    # Heading: 1–6 # characters, followed by a space
    if len(lines) == 1:
        line = lines[0]
        for i in range(1, 7):
            if line.startswith("#" * i + " "):
                return BlockType.HEADING

    # Quote block: every line starts with >
    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE

    # Unordered list: every line starts with "- "
    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST

    # Ordered list: 1. 2. 3. ... incrementing by 1
    ordered = True
    for i, line in enumerate(lines, start=1):
        if not line.startswith(f"{i}. "):
            ordered = False
            break
    if ordered:
        return BlockType.ORDERED_LIST

    # Default
    return BlockType.PARAGRAPH

def text_to_children(text):
    text_nodes = inline_markdown.text_to_textnodes(text)
    children = []
    for tn in text_nodes:
        children.append(text_node_to_html_node(tn))
    return children

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []

    for block in blocks:
        block_type = block_to_block_type(block)

        if block_type == BlockType.PARAGRAPH:
            node = ParentNode("p", text_to_children(block))

        elif block_type == BlockType.HEADING:
            level = len(block.split(" ")[0])
            text = block[level + 1 :]
            node = ParentNode(f"h{level}", text_to_children(text))

        elif block_type == BlockType.CODE:
            text = block.strip("`").lstrip("\n")
            text_node = TextNode(text, TextType.TEXT)
            code_node = ParentNode(
                "code",
                [text_node_to_html_node(text_node)],
            )
            node = ParentNode("pre", [code_node])

        elif block_type == BlockType.QUOTE:
            text = "\n".join(line.lstrip("> ") for line in block.split("\n"))
            node = ParentNode("blockquote", text_to_children(text))

        elif block_type == BlockType.UNORDERED_LIST:
            items = []
            for line in block.split("\n"):
                items.append(
                    ParentNode("li", text_to_children(line[2:]))
                )
            node = ParentNode("ul", items)

        elif block_type == BlockType.ORDERED_LIST:
            items = []
            for line in block.split("\n"):
                items.append(
                    ParentNode("li", text_to_children(line.split(". ", 1)[1]))
                )
            node = ParentNode("ol", items)

        else:
            raise ValueError(f"Unknown block type: {block_type}")

        children.append(node)

    return ParentNode("div", children)
