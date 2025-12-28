from htmlnode import HTMLNode

def test_props_to_html_basic():
    node = HTMLNode(
        tag="a",
        props={"href": "https://google.com", "target": "_blank"}
    )
    result = node.props_to_html()
    assert result == ' href="https://google.com" target="_blank"'

def test_props_to_html_empty():
    node = HTMLNode(tag="p", props={})
    assert node.props_to_html() == ""

def test_repr_includes_all_fields():
    node = HTMLNode(
        tag="p",
        value="Hello",
        children=None,
        props={"class": "text"}
    )
    rep = repr(node)
    assert "tag='p'" in rep
    assert "value='Hello'" in rep
    assert "props={'class': 'text'}" in rep
