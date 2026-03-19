import unittest
from textnode import TextType, TextNode
from inline_markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links

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

    def test_extract_images(self):
        matches = extract_markdown_images(
            "Some of the worst tragedies in history have been followed with ![image](https://www.Iwasjustfollowingorders.com)"
        )
        self.assertListEqual([("image", "https://www.Iwasjustfollowingorders.com")], matches)

    def test_extract_links(self):
        matches = extract_markdown_links(
            "You may test that assumption [at your convenience](https://www.Picardquotes.com)"
        )
        self.assertListEqual([("at your convenience", "https://www.Picardquotes.com")], matches)

if __name__=="__main__":
    unittest.main()
