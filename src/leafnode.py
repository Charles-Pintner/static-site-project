from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        if value is None:
            raise ValueError("invalid HTML: no value")
        # Leaf nodes never have children, so pass [] for children
        super().__init__(tag, value, [], props)

    def to_html(self):
        # No need to re-check value here, the constructor guarantees it
        if self.tag is None:
            return self.value
        props = self.props_to_html()
        return f"<{self.tag}{props}>{self.value}</{self.tag}>"
