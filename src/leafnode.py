from htmlnode import HTMLNode
class LeafNode(HTMLNode):
    def __init__(self, tag, value, attributes=None):
        super().__init__(tag, value, attributes)
        if value is None:
            raise ValueError("LeafNode must have a value")

    def to_html(self):
        if not self.tag:
            return self.value
        props = self.props_to_html()
        if props:
            return f"<{self.tag} {props}>{self.value}</{self.tag}>"
        else:
            return f"<{self.tag}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode(tag={self.tag}, value={self.value}, attributes={self.attributes})"

    def __eq__(self, other):
        if not isinstance(other, LeafNode):
            return False
        return (self.tag == other.tag and
                self.value == other.value and
                self.attributes == other.attributes)