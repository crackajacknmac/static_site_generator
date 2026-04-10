from enum import Enum

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
