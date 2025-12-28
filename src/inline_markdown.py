import re
from typing import List
from textnode import TextNode, TextType

def text_to_textnodes(text: str):
    """
    Take a raw markdown string and return a list of TextNode objects
    with all the inline markdown parsed.
    """
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    """
    Split TextType.TEXT nodes based on the given delimiter and assign
    the inner content the provided text_type.
    
    old_nodes: list[TextNode]
    delimiter: string delimiter to split on (e.g., "`", "**", "_")
    text_type: TextType to apply to delimited text
    """
    new_nodes = []

    for node in old_nodes:
        # Only operate on plain text nodes
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        # If delimiter not present, no splitting needed
        if delimiter not in node.text:
            new_nodes.append(node)
            continue

        parts = node.text.split(delimiter)

        # Even indices: normal text
        # Odd indices: delimited text
        if len(parts) % 2 == 0:
            raise Exception(
                f"Invalid Markdown syntax: unmatched delimiter '{delimiter}' in: {node.text!r}"
            )

        for i, part in enumerate(parts):
            if part == "":
                continue  # ignore empty segments (e.g., leading or trailing)

            if i % 2 == 0:
                # Outside delimiters ⇒ normal text
                new_nodes.append(TextNode(part, TextType.TEXT))
            else:
                # Inside delimiters ⇒ formatted text
                new_nodes.append(TextNode(part, text_type))

    return new_nodes

def extract_markdown_images(text):
    """
    Extract markdown images of the form:
    ![alt text](url)

    Returns: list of (alt_text, url)
    """
    pattern = r'!\[([^\]]*)\]\(([^)]+)\)'
    return re.findall(pattern, text)

def extract_markdown_links(text):
    """
    Extract markdown links of the form:
    [anchor text](url)

    Returns: list of (anchor_text, url)
    """
    pattern = r'(?<!!)\[([^\]]+)\]\(([^)]+)\)'
    return re.findall(pattern, text)


IMAGE_PATTERN = re.compile(r"!\[([^\]]+)\]\(([^)]+)\)")
LINK_PATTERN = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")

def split_nodes_image(old_nodes: List[TextNode]) -> List[TextNode]:
    """
    Split nodes by extracting Markdown images: ![alt](url)
    """
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        text = node.text
        pos = 0

        for match in IMAGE_PATTERN.finditer(text):
            start, end = match.span()
            alt_text, url = match.groups()

            # Add text before the image
            if start > pos:
                new_nodes.append(TextNode(text[pos:start], TextType.TEXT))

            # Add the IMAGE node
            new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))

            pos = end

        # Add any remaining trailing text
        if pos < len(text):
            new_nodes.append(TextNode(text[pos:], TextType.TEXT))

    return new_nodes


def split_nodes_link(old_nodes: List[TextNode]) -> List[TextNode]:
    """
    Split nodes by extracting Markdown links: [text](url)
    """
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        text = node.text
        pos = 0

        for match in LINK_PATTERN.finditer(text):
            start, end = match.span()
            link_text, url = match.groups()

            # Add text before the link
            if start > pos:
                new_nodes.append(TextNode(text[pos:start], TextType.TEXT))

            # Add the LINK node
            new_nodes.append(TextNode(link_text, TextType.LINK, url))

            pos = end

        # Add trailing text
        if pos < len(text):
            new_nodes.append(TextNode(text[pos:], TextType.TEXT))

    return new_nodes
