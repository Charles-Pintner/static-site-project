from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        if tag is None:
            raise ValueError("ParentNode requires a tag")
        if children is None:
            raise ValueError("ParentNode requires children")

        # parent nodes do not take a value
        super().__init__(tag=tag, value=None, children=children, props=props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("ParentNode must have a tag to render HTML")

        if self.children is None:
            raise ValueError("ParentNode must have children to render HTML")

        # Recursively build HTML from each child
        inner_html = ""
        for child in self.children:
            inner_html += child.to_html()

        props = self.props_to_html()
        return f"<{self.tag}{props}>{inner_html}</{self.tag}>"
