class HTMLNode:
    def __init__(self, tag = None, value = None, attributes =None, children=None):
        self.tag = tag
        self.value = value
        self.attributes = attributes
        self.children = children
    def to_html(self):
        raise NotImplementedError("Subclasses should implement this method")

    def props_to_html(self):
        if not self.attributes:
            return ""
        props = []
        for key, value in self.attributes.items():
            props.append(f'{key}="{value}"')
        return " ".join(props)\

    def __repr__(self):
        return f"HTMLNode(tag={self.tag}, value={self.value}, attributes={self.attributes}, children={self.children})"

    def __eq__(self, other):
        if not isinstance(other, HTMLNode):
            return False
        return (self.tag, self.value, self.attributes, self.children) == (other.tag, other.value, other.attributes, other.children)
