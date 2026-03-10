import unittest

from htmlnode import HTMLNode


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


if __name__ == "__main__":
    unittest.main()
