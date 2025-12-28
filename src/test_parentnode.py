import unittest
from leafnode import LeafNode
from parentnode import ParentNode


class TestParentNode(unittest.TestCase):

    # Provided tests
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    # Additional tests
    def test_parentnode_requires_tag(self):
        with self.assertRaises(ValueError):
            ParentNode(None, [])

    def test_parentnode_requires_children(self):
        with self.assertRaises(ValueError):
            ParentNode("div", None)

    def test_parentnode_empty_children_list(self):
        # empty list is allowed
        node = ParentNode("div", [])
        self.assertEqual(node.to_html(), "<div></div>")

    def test_multiple_children(self):
        node = ParentNode("p", [
            LeafNode("b", "Bold"),
            LeafNode(None, " text "),
            LeafNode("i", "italic")
        ])
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold</b> text <i>italic</i></p>"
        )

    def test_nested_parentnodes(self):
        node = ParentNode("div", [
            ParentNode("section", [
                ParentNode("article", [
                    LeafNode("p", "Deep content")
                ])
            ])
        ])
        self.assertEqual(
            node.to_html(),
            "<div><section><article><p>Deep content</p></article></section></div>"
        )

    def test_parentnode_with_props(self):
        node = ParentNode("div", [
            LeafNode("p", "hello")
        ], {"class": "container", "id": "main"})
        self.assertEqual(
            node.to_html(),
            '<div class="container" id="main"><p>hello</p></div>'
        )


if __name__ == "__main__":
    unittest.main()
