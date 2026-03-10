import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("This is some text", TextType.ITALIC)
        node2 = TextNode("This is some text", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_empty_url(self):
        node = TextNode("More random text", TextType.PLAIN)
        self.assertIsNone(node.url)



if __name__ == "__main__":
    unittest.main()
