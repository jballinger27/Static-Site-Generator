import unittest
from blocktype import block_to_blockType, BlockType

class TestBlockToBlockType(unittest.TestCase):
    def test_header(self):
        self.assertEqual(block_to_blockType("# Header"), BlockType.HEADER)

    def test_unordered_list(self):
        block = "- item1\n- item2\n- item3"
        self.assertEqual(block_to_blockType(block), BlockType.UNORDERED_LIST)

    def test_unordered_list_with_invalid_line(self):
        block = "- item1\nnot a list item\n- item3"
        self.assertEqual(block_to_blockType(block), BlockType.PARAGRAPH)

    def test_ordered_list(self):
        block = "1. item1\n2. item2\n3. item3"
        self.assertEqual(block_to_blockType(block), BlockType.ORDERED_LIST)

    def test_ordered_list_with_invalid_line(self):
        block = "1. item1\n2. item2\nnot a list item"
        self.assertEqual(block_to_blockType(block), BlockType.PARAGRAPH)

    def test_quote(self):
        block = "> quote line 1\n> quote line 2"
        self.assertEqual(block_to_blockType(block), BlockType.QUOTE)

    def test_quote_with_invalid_line(self):
        block = "> quote line 1\nnot a quote"
        self.assertEqual(block_to_blockType(block), BlockType.PARAGRAPH)

    def test_code_block(self):
        block = "```\ncode line 1\ncode line 2\n```"
        self.assertEqual(block_to_blockType(block), BlockType.CODE)

    def test_paragraph(self):
        block = "This is a paragraph."
        self.assertEqual(block_to_blockType(block), BlockType.PARAGRAPH)

if __name__ == "__main__":
    unittest.main()