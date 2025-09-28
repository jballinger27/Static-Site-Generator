import unittest
from parentnode import ParentNode
from htmlnode import HTMLNode
from leafnode import LeafNode
class DummyNode(HTMLNode):
    def __init__(self, html):
        super().__init__(None)
        self.html = html

    def to_html(self):
        return self.html

class TestParentNode(unittest.TestCase):
    def test_to_html_with_props(self):
        children = [DummyNode("Hello"), DummyNode("World")]
        props = {"class": "my-class", "id": "main"}
        node = ParentNode("div", children, props)
        expected = '<div class="my-class" id="main">HelloWorld</div>'
        self.assertEqual(node.to_html(), expected)

    def test_to_html_without_props(self):
        children = [DummyNode("A"), DummyNode("B")]
        node = ParentNode("span", children)
        expected = '<span>AB</span>'
        self.assertEqual(node.to_html(), expected)

    def test_to_html_raises_no_tag(self):
        children = [DummyNode("X")]
        node = ParentNode(None, children)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_raises_no_children(self):
        node = ParentNode("p", [])
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_nested(self):
        inner = ParentNode("b", [DummyNode("Bold")])
        outer = ParentNode("div", [DummyNode("Start"), inner, DummyNode("End")])
        expected = '<div>Start<b>Bold</b>End</div>'
        self.assertEqual(outer.to_html(), expected)

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
    def test_to_html_multiple_leaf_and_parent_nodes(self):
        leaf1 = LeafNode("span", "first")
        leaf2 = LeafNode("span", "second")
        parent = ParentNode("div", [leaf1, leaf2])
        expected = "<div><span>first</span><span>second</span></div>"
        self.assertEqual(parent.to_html(), expected)

    def test_to_html_deeply_nested_parent_and_leaf_nodes(self):
        leaf = LeafNode("em", "deep")
        inner_parent = ParentNode("span", [leaf])
        middle_parent = ParentNode("p", [inner_parent])
        outer_parent = ParentNode("div", [middle_parent])
        expected = "<div><p><span><em>deep</em></span></p></div>"
        self.assertEqual(outer_parent.to_html(), expected)

if __name__ == "__main__":
    unittest.main()