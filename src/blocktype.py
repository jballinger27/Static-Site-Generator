from enum import Enum
import re
class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADER = "header"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"
    QUOTE = "quote"
    CODE = "code"


def block_to_blockType(block):
    if block.startswith("#"):
        return BlockType.HEADER
    elif block.startswith("- "):
        for line in block.splitlines():
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST
    elif block.startswith("1. "):
        for line in block.splitlines():
            if not re.match(r"^\d+\. ", line):
                return BlockType.PARAGRAPH
        return BlockType.ORDERED_LIST
    elif block.startswith("> "):
        for line in block.splitlines():
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    elif block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    else:
        return BlockType.PARAGRAPH