import unittest
from main import *
from textnode import TextNode, TextType
from leafnode import LeafNode
from texttohtml import text_node_to_html_node, text_to_textnodes

class TestTextNodeToHtmlNode(unittest.TestCase):
    def test_plain_text(self):
        tn = TextNode("Hello", TextType.TEXT)
        node = text_node_to_html_node(tn)
        self.assertIsInstance(node, LeafNode)
        self.assertIsNone(node.tag)
        self.assertEqual(node.value, "Hello")

    def test_bold_text(self):
        tn = TextNode("Bold", TextType.BOLD)
        node = text_node_to_html_node(tn)
        self.assertEqual(node.tag, "b")
        self.assertEqual(node.value, "Bold")

    def test_italic_text(self):
        tn = TextNode("Italic", TextType.ITALIC)
        node = text_node_to_html_node(tn)
        self.assertEqual(node.tag, "i")
        self.assertEqual(node.value, "Italic")

    def test_underline_text(self):
        tn = TextNode("Underline", TextType.UNDERLINE)
        node = text_node_to_html_node(tn)
        self.assertEqual(node.tag, "u")
        self.assertEqual(node.value, "Underline")

    def test_link_text(self):
        tn = TextNode("Link", TextType.LINK, "https://example.com")
        node = text_node_to_html_node(tn)
        self.assertEqual(node.tag, "a")
        self.assertEqual(node.value, "Link")
        self.assertEqual(node.attributes, {"href": "https://example.com"})

    def test_code_text(self):
        tn = TextNode("print('hi')", TextType.CODE)
        node = text_node_to_html_node(tn)
        self.assertEqual(node.tag, "code")
        self.assertEqual(node.value, "print('hi')")

    def test_image_text(self):
        tn = TextNode("alt text", TextType.IMAGE, "img.png")
        node = text_node_to_html_node(tn)
        self.assertEqual(node.tag, "img")
        self.assertEqual(node.value, "")
        self.assertEqual(node.attributes, {"src": "img.png", "alt": "alt text"})

    def test_unsupported_type(self):
        class DummyType:
            pass
        tn = TextNode("dummy", DummyType)
        with self.assertRaises(ValueError):
            text_node_to_html_node(tn)

class TestTextToTextNodes(unittest.TestCase):
    def test_plain_text(self):
        text = "This is plain text."
        nodes = text_to_textnodes(text)
        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0], TextNode(text, TextType.TEXT))

    def test_delim_bold(self):
        node = TextNode("This is text with **bold** and **another** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_single(self):
        node = TextNode("This is text with **bold** and another", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" and another", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_multiple(self):
        node = TextNode("This is text with **bold** and **another**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_bold_adjacent(self):
        node = TextNode("This is text with **bold****another**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes)

    def test_image(self):
        node = TextNode("This is text with an image ![alt text](image.png) in it", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an image ", TextType.TEXT),
                TextNode("alt text", TextType.IMAGE, "image.png"),
                TextNode(" in it", TextType.TEXT),
            ],
            new_nodes,
        )
    def test_image_multiple(self):
        node = TextNode("Image1 ![alt1](img1.png) and Image2 ![alt2](img2.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("Image1 ", TextType.TEXT),
                TextNode("alt1", TextType.IMAGE, "img1.png"),
                TextNode(" and Image2 ", TextType.TEXT),
                TextNode("alt2", TextType.IMAGE, "img2.png"),
            ],
            new_nodes,
        )

    def test_image_no_image(self):
        node = TextNode("This is text without an image", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [TextNode("This is text without an image", TextType.TEXT)],
            new_nodes,
        )

    def test_link(self):
        node = TextNode("This is text with a [link](https://example.com) in it", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://example.com"),
                TextNode(" in it", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_link_multiple(self):
        node = TextNode("Link1 [link1](https://link1.com) and Link2 [link2](https://link2.com)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Link1 ", TextType.TEXT),
                TextNode("link1", TextType.LINK, "https://link1.com"),
                TextNode(" and Link2 ", TextType.TEXT),
                TextNode("link2", TextType.LINK, "https://link2.com"),
            ],
            new_nodes,
        )

    def test_link_no_link(self):
        node = TextNode("This is text without a link", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [TextNode("This is text without a link", TextType.TEXT)],
            new_nodes,
        )

    def test_combined(self):
        text = "This is **bold** text with a [link](https://example.com) and an ![image](img.png)."
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://example.com"),
                TextNode(" and an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "img.png"),
                TextNode(".", TextType.TEXT),
            ],
            nodes,
        )

    def test_no_inline(self):
        text = "This is plain text without any inline markdown."
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            [TextNode(text, TextType.TEXT)],
            nodes,
        )

if __name__ == "__main__":
    unittest.main()