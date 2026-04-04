from enum import Enum
from block_helper import is_heading, is_code_block, is_quote, is_ulist, is_olist

def markdown_to_blocks(document):
    output = []
    blocks = document.split("\n\n")
    for block in blocks:
        block = block.strip()
        if len(block) > 0:
            output.append(block)
    return output

class BlockType(Enum):
    PARAGRAPH = "<p>"
    HEADING = "<h1>"
    CODE = "<code>"
    QUOTE = "<blockquote>"
    ULIST = "<ul>"
    OLIST = "<ol>"

def block_to_block_type(text):
    if text.startswith("#"):
        return BlockType.HEADING if is_heading(text) else BlockType.PARAGRAPH
    elif text.startswith("`"):
        return BlockType.CODE if is_code_block(text) else BlockType.PARAGRAPH
    elif text.startswith(">"):
        return BlockType.QUOTE if is_quote(text) else BlockType.PARAGRAPH
    elif text.startswith("-"):
        return BlockType.ULIST if is_ulist(text) else BlockType.PARAGRAPH
    else:
        return BlockType.OLIST if is_olist(text) else BlockType.PARAGRAPH
    