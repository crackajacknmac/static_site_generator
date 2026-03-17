import unittest
from textnode import TextType, TextNode
from inline_markdown import split_nodes_delimiter

class TestInline(unittest.TestCase):
    def test_normal_output(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
        new_nodes,
        [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT)
        ],
    )

    def test_flawed_output(self):
        node = TextNode("This is some **plain text", TextType.TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "**", TextType.BOLD)

    def test_bold(self):
        node = TextNode("To **boldly** go where no man has gone before!", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
        new_nodes,
        [
            TextNode("To ", TextType.TEXT),
            TextNode("boldly", TextType.BOLD),
            TextNode(" go where no man has gone before!", TextType.TEXT)
        ],
    )


if __name__=="__main__":
    unittest.main()
