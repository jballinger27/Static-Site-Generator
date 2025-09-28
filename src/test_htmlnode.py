import unittest
from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_init_defaults(self):
        node = HTMLNode()
        self.assertIsNone(node.tag)
        self.assertIsNone(node.value)
        self.assertIsNone(node.attributes)
        self.assertIsNone(node.children)

    def test_init_with_values(self):
        node = HTMLNode(
            tag="div",
            value="Hello",
            attributes={"class": "greeting"},
            children=[HTMLNode(tag="span", value="World")]
        )
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.value, "Hello")
        self.assertEqual(node.attributes, {"class": "greeting"})
        self.assertEqual(len(node.children), 1)
        self.assertIsInstance(node.children[0], HTMLNode)

    def test_props_to_html_empty(self):
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_with_attributes(self):
        node = HTMLNode(attributes={"id": "main", "class": "container"})
        props_html = node.props_to_html()
        self.assertIn('id="main"', props_html)
        self.assertIn('class="container"', props_html)
        self.assertTrue(props_html == 'id="main" class="container"' or props_html == 'class="container" id="main"')

    def test_repr(self):
        node = HTMLNode(tag="p", value="Text", attributes={"style": "color:red;"})
        expected = "HTMLNode(tag=p, value=Text, attributes={'style': 'color:red;'}, children=None)"
        self.assertEqual(repr(node), expected)

    def test_eq_true(self):
        node1 = HTMLNode(tag="a", value="Link", attributes={"href": "#"})
        node2 = HTMLNode(tag="a", value="Link", attributes={"href": "#"})
        self.assertEqual(node1, node2)

    def test_eq_false(self):
        node1 = HTMLNode(tag="a", value="Link", attributes={"href": "#"})
        node2 = HTMLNode(tag="a", value="Link", attributes={"href": "/home"})
        self.assertNotEqual(node1, node2)

    def test_to_html_not_implemented(self):
        node = HTMLNode()
        with self.assertRaises(NotImplementedError):
            node.to_html()

if __name__ == "__main__":
    unittest.main()