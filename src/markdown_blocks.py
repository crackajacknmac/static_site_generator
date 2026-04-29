from enum import Enum
from textnode import TextNode, TextType, text_node_to_html_node
from htmlnode import HTMLNode, ParentNode
from inline_markdown import text_to_textnodes

class BlockType(Enum):
        PARAGRAPH = "paragraph"
        HEADING = "heading"
        CODE = "code"
        QUOTE = "quote"
        UNORDERED_LIST = "unordered_list"
        ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown):
    final_blocks = []
    raw_blocks = markdown.split("\n\n")
    for block in raw_blocks:
        block = block.strip()
        final_blocks.append(block)
    return list(filter(None, final_blocks))

def block_to_block_type(block):
    if block.startswith("```\n") and block.endswith("```"):
        return BlockType.CODE

    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING

    if block.startswith(">"):
        lines = block.split("\n")
        for line in lines:
            if line.startswith(">"):
                continue
            else:
                return BlockType.PARAGRAPH
        return BlockType.QUOTE

    if block.startswith("- "):
        lines = block.split("\n")
        for line in lines:
            if line.startswith("- "):
                continue
            else:
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST

    if block.startswith("1. "):
        lines = block.split("\n")
        number = 1
        for line in lines:
            if line.startswith(f"{number}. "):
                number += 1
                continue
            else:
                return BlockType.PARAGRAPH
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH


def text_to_children(block):
    children_nodes = []
    raw_children_nodes = text_to_textnodes(block)
    for child in raw_children_nodes:
        child_node = text_node_to_html_node(child)
        children_nodes.append(child_node)
    return children_nodes

def text_to_parent(block):
    block_type = block_to_block_type(block)
    if block_type == BlockType.PARAGRAPH:
        paragraph_text = block.replace("\n", " ")
        parent_node = ParentNode("p", text_to_children(paragraph_text))
        return parent_node
    elif block_type == BlockType.HEADING:
        hashes, rest = block.split(" ", 1)
        level = len(hashes)
        parent_node = ParentNode(f"h{level}", text_to_children(rest))
        return parent_node
    elif block_type == BlockType.QUOTE:
        cleaned_lines = []
        lines = block.split("\n")
        for line in lines:
            if not line.startswith(">"):
                raise ValueError("invalid quote block")
            cleaned_lines.append(line.lstrip(">").strip())
        joined = " ".join(cleaned_lines)
        parent_node = ParentNode("blockquote", text_to_children(joined))
        return parent_node
    elif block_type == BlockType.UNORDERED_LIST:
        children_lines = []
        lines = block.split("\n")
        for line in lines:
            clean_line = line[2:]
            text_line = text_to_children(clean_line)
            list_item = ParentNode("li", text_line)
            children_lines.append(list_item)
        parent_node = ParentNode("ul", children_lines)
        return parent_node
    elif block_type == BlockType.ORDERED_LIST:
        children_lines = []
        lines = block.split("\n")
        for line in lines:
            clean_line = line[3:]
            text_line = text_to_children(clean_line)
            list_item = ParentNode("li", text_line)
            children_lines.append(list_item)
        parent_node = ParentNode("ol", children_lines)
        return parent_node
    elif block_type == BlockType.CODE:
        if not block.startswith("```") or not block.endswith("```"):
            raise ValueError("not a valid code block")
        sliced = block[4:-3]
        new_node = TextNode(sliced, TextType.TEXT)
        growing_node = text_node_to_html_node(new_node)
        adult_node = ParentNode("code", [growing_node])
        parent_node = ParentNode("pre", [adult_node])
        return parent_node

def markdown_to_html_node(markdown):
    content_nodes = []
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        content_node = text_to_parent(block)
        content_nodes.append(content_node)
    page_content = ParentNode("div", content_nodes)
    return page_content
