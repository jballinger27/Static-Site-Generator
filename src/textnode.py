from enum import Enum

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    UNDERLINE = "underline"
    LINK = "link"
    CODE = "code"
    IMAGE = "image"


class TextNode:
    def __init__(self, text: str, text_type: TextType = TextType.TEXT, href = None):
        self.text = text
        self.text_type = text_type
        self.href = href  # Used for links and images

    def __eq__(self, other):
        if not isinstance(other, TextNode):
            return False
        return (self.text, self.text_type, self.href) == (other.text, other.text_type, other.href)

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.href})"