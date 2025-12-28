from textnode import TextNode, TextType
from splitter import (
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
)


def text_to_textnodes(text: str):
    """
    Convert full Markdown-like text into a list of TextNodes.
    """

    # Start with a single text node
    nodes = [TextNode(text, TextType.TEXT)]

    # Apply splits in order
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)

    # Bold (**)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)

    # Italic (_)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)

    # Code (`...`)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)

    return nodes
