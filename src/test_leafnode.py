import unittest
from leafnode import LeafNode
from htmlnode import *
import sys

class DummyHTMLNode:
    def __init__(self, tag, value, attributes=None):
        self.tag = tag
        self.value = value
        self.attributes = attributes or {}

# Patch HTMLNode for testing if needed
#sys.modules['leafnode'].HTMLNode = DummyHTMLNode

class TestLeafNode(unittest.TestCase):
    def test_leafnode_init_sets_attributes(self):
        node = LeafNode("p", "Hello", {"class": "greeting"})
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, "Hello")
        self.assertEqual(node.attributes, {"class": "greeting"})

    def test_leafnode_init_raises_value_error_on_none_value(self):
        with self.assertRaises(ValueError):
            LeafNode("p", None)

    def test_leafnode_to_html_with_tag_and_attributes(self):
        node = LeafNode("span", "World", {"id": "test"})
        node.props_to_html = lambda: 'id="test"'
        self.assertEqual(node.to_html(), '<span id="test">World</span>')

    def test_leafnode_to_html_with_tag_no_attributes(self):
        node = LeafNode("div", "Content")
        node.props_to_html = lambda: ''
        self.assertEqual(node.to_html(), '<div>Content</div>')

    def test_leafnode_to_html_without_tag(self):
        node = LeafNode(None, "Just text")
        self.assertEqual(node.to_html(), "Just text")

    def test_leafnode_repr(self):
        node = LeafNode("h1", "Title", {"style": "bold"})
        self.assertEqual(repr(node), "LeafNode(tag=h1, value=Title, attributes={'style': 'bold'})")

    def test_leafnode_eq_true(self):
        node1 = LeafNode("a", "Link", {"href": "url"})
        node2 = LeafNode("a", "Link", {"href": "url"})
        self.assertEqual(node1, node2)

    def test_leafnode_eq_false_different_tag(self):
        node1 = LeafNode("a", "Link", {"href": "url"})
        node2 = LeafNode("span", "Link", {"href": "url"})
        self.assertNotEqual(node1, node2)

    def test_leafnode_eq_false_different_value(self):
        node1 = LeafNode("a", "Link", {"href": "url"})
        node2 = LeafNode("a", "Other", {"href": "url"})
        self.assertNotEqual(node1, node2)

    def test_leafnode_eq_false_different_attributes(self):
        node1 = LeafNode("a", "Link", {"href": "url"})
        node2 = LeafNode("a", "Link", {"href": "other"})
        self.assertNotEqual(node1, node2)

    def test_leafnode_eq_false_other_type(self):
        node = LeafNode("a", "Link", {"href": "url"})
        self.assertNotEqual(node, "not a node")

if __name__ == "__main__":
    unittest.main()