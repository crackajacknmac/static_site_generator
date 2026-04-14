import unittest
from markdown_blocks import markdown_to_blocks, BlockType, block_to_block_type

class TestMarkdown(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )



    def test_block_to_block_type_heading(self):
        block = "#### This is a heading"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.HEADING)

    def test_block_to_block_type_quote(self):
        block = ">There are no accidents. -Master Oogway."
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.QUOTE)

    def test_block_to_block_type_code(self):
        block = "```\nThis is a code block\n```"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.CODE)

    def test_block_to_block_type_unordered_list(self):
        block = "- This is a list\n- Tomato paste\n- Carrots\n- Grape jelly"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.UNORDERED_LIST)

    def test_block_to_block_type_ordered_list(self):
        block = "1. This is an ordered list.\n2. It needs to be tested\n3. So let's test it."
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.ORDERED_LIST)

    def test_block_to_block_type_paragraph(self):
        block = "This is some text"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.PARAGRAPH)
