def markdown_to_blocks(markdown):
    final_blocks = []
    raw_blocks = markdown.split("\n\n")
    for block in raw_blocks:
        block = block.strip()
        final_blocks.append(block)
    return list(filter(None, final_blocks))
