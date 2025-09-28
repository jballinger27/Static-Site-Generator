import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

        node = TextNode("This is a text node!", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)
        self.assertNotEqual(
            TextNode("This is a text node", TextType.LINK, "https://www.boot.dev"),
            TextNode("This is a text node", TextType.LINK, "https://www.example.com")
        )

        self.assertNotEqual(
            TextNode("This is a text node", TextType.LINK, "https://www.boot.dev"),
            TextNode("This is a text node", TextType.TEXT)
        )

    def test_link(self):
        node = TextNode("This is a text node", TextType.LINK, "https://www.boot.dev")
        node2 = TextNode("This is a text node", TextType.LINK, "https://www.boot.dev")
        self.assertEqual(node, node2)

        self.assertNotEqual(node.href, None)

    def test_italic(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertEqual(node, node2)

    def test_image(self):
        node = TextNode("This is a text node", TextType.IMAGE, "https://www.boot.dev/image.png")
        node2 = TextNode("This is a text node", TextType.IMAGE, "https://www.boot.dev/image.png")
        self.assertEqual(node, node2)
        self.assertNotEqual(node.href, None)

    def test_NotEqual(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)


if __name__ == "__main__":
    unittest.main()