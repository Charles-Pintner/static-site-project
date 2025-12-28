class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        print("DEBUG LeafNode.to_html called with value:", self.value)
        """Child classes will implement this. Base class should not render HTML."""
        raise NotImplementedError("to_html() must be implemented by child classes.")

    def props_to_html(self):
        """Convert props dict to HTML attributes string.

        Example:
            {"href": "https://google.com", "target": "_blank"}
            → ' href="https://google.com" target="_blank"'
        """
        if not self.props:
            return ""

        attributes = []
        for key, value in self.props.items():
            attributes.append(f'{key}="{value}"')

        return " " + " ".join(attributes)

    def __repr__(self):
        return f"HTMLNode(tag={self.tag!r}, value={self.value!r}, children={self.children!r}, props={self.props!r})"


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("invalid HTML: no value")
        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("invalid HTML: no tag")
        if self.children is None:
            raise ValueError("invalid HTML: no children")

        children_html = ""
        for child in self.children:
            if child is None:
                print("Found None child in ParentNode:", self.tag)
            children_html += child.to_html()

        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"

    def __repr__(self):
        return f"ParentNode({self.tag}, children: {self.children}, props: {self.props})"
