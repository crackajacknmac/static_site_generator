import unittest

from htmlnode import HTMLNode, LeafNode

class TestHtmlNode(unittest.TestCase):

    def test_empty_children(self):
        node = HTMLNode("More random text", "value is nothing here")
        self.assertIsNone(node.children)

    def test_props_to_html(self):
        node = HTMLNode("a", "Google", None, {"href": "https://www.google.com"})
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com"')

    def test_props_to_html_again(self):
        node = HTMLNode("text", "serebii", None, {"href": "https://www.serebii.com"})
        self.assertEqual(node.props_to_html(), ' href="https://www.serebii.com"')


class TestLeafNode(unittest.TestCase):

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_no_tag(self):
        node = LeafNode(None, "Hello, Hello")
        self.assertEqual(node.to_html(), "Hello, Hello")

    def test_no_value(self):
        node = LeafNode("a", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_with_props(self):
        node = LeafNode("p", "Hello again", {"href": "http://www.wikipedia.com"})
        self.assertEqual(node.to_html(), '<p href="http://www.wikipedia.com">Hello again</p>')

if __name__ == "__main__":
    unittest.main()
