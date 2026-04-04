from block_extraction import markdown_to_blocks, block_to_block_type, BlockType
from extraction import text_to_textnodes
from textnode import text_node_to_html_node
from htmlnode import ParentNode, LeafNode

# converts a full markdown document into a single parent HTMLNode. 
# That one parent HTMLNode should (obviously) contain many child HTMLNode objects representing the nested elements.
def markdown_to_html_node(document):
    children = []
    blocks = markdown_to_blocks(document)
    for block in blocks:
        block_type = block_to_block_type(block)
        html_node = block_to_html_node(block, block_type)
        children.append(html_node)
    return ParentNode("div", children)


def text_to_children(text):
    output = []
    text_nodes = text_to_textnodes(text)
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        output.append(html_node)
    return output

def block_to_html_node(block_text, type):
    if type == BlockType.PARAGRAPH:
        text_no_new_line = squash_paragraph_new_lines(block_text)
        children = text_to_children(text_no_new_line)
        return ParentNode("p", children)
    elif type == BlockType.HEADING:
        # count how many '#' are there
        separated = block_text.split(" ", 1)
        children = text_to_children(separated[1])
        return ParentNode(f"h{len(separated[0])}", children)
    elif type == BlockType.QUOTE:
        children = parse_quote_items_to_html_nodes(block_text)
        return ParentNode("blockquote", children)
    elif type == BlockType.ULIST:
        children = parse_list_items_to_html_nodes(block_text)
        return ParentNode("ul", children)
    elif type == BlockType.OLIST:
        children = parse_list_items_to_html_nodes(block_text)
        return ParentNode("ol", children)
    elif type == BlockType.CODE:
        code_text = parse_code_block(block_text)
        child = LeafNode("code", code_text)
        return ParentNode("pre", [child])


def parse_list_items_to_html_nodes(text):
    output = []
    list_items = text.split("\n")
    for item in list_items:
        separated = item.split(" ", 1)
        if len(separated) > 1:
            output.append(ParentNode("li", text_to_children(separated[1])))
    return output

def parse_quote_items_to_html_nodes(text):
    output = []
    list_items = text.split("\n")
    for item in list_items:
        separated = item.split(" ", 1)
        if len(separated) > 1:
            output.append(f"{separated[1]}")
    return text_to_children(" ".join(output))

def parse_code_block(text):
    start_index = 4 # skipping ```\n
    end_index = -3 # skipping ```
    return text[start_index : end_index]

def squash_paragraph_new_lines(text):
    output = []
    lines = text.split("\n")
    for line in lines:
        if len(line):
            output.append(line)
    return " ".join(output)