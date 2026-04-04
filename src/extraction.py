# importing regex
import re
from textnode import TextNode, TextType, split_nodes_delimiter

def extract_markdown_images(text):
    matches = re.findall(r"!\[(.*?)\]\((.+?)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[(.*?)\]\((.+?)\)", text)
    return matches

def split_nodes_image(nodes):
    output = []
    for node in nodes:
        if node.text_type != TextType.TEXT:
            output.append(node)
            continue
        images = extract_markdown_images(node.text)
        text = node.text
        part1 = ""
        part2 = ""
        for i in range(len(images)):
            delim = f"![{images[i][0]}]({images[i][1]})"
            part1, part2 = text.split(delim, 1)
            if len(part1) > 0:
                output.append(TextNode(part1, TextType.TEXT))
            output.append(TextNode(images[i][0], TextType.IMAGE, images[i][1]))
            text = part2
        if len(text) > 0:
            output.append(TextNode(text, TextType.TEXT))
    return output

def split_nodes_link(nodes):
    output = []
    for node in nodes:
        if node.text_type != TextType.TEXT:
            output.append(node)
            continue
        links = extract_markdown_links(node.text)
        text = node.text
        part1 = ""
        part2 = ""
        for i in range(len(links)):
            delim = f"[{links[i][0]}]({links[i][1]})"
            part1, part2 = text.split(delim, 1)
            if len(part1) > 0:
                output.append(TextNode(part1, TextType.TEXT))
            output.append(TextNode(links[i][0], TextType.LINK, links[i][1]))
            text = part2
        if len(text) > 0:
            output.append(TextNode(text, TextType.TEXT))
    return output
    

# get a text and convert it to necessary TextNodes
def text_to_textnodes(text):
    bold_delim = "**"
    italic_delim = "_"
    code_delim = "`"
    node = TextNode(text, TextType.TEXT)
    try:
        after_bold = split_nodes_delimiter([node], bold_delim, TextType.BOLD)
        after_italic = split_nodes_delimiter(after_bold, italic_delim, TextType.ITALIC)
        after_code = split_nodes_delimiter(after_italic, code_delim, TextType.CODE)
        after_image_extracted = split_nodes_image(after_code)
        after_link_extracted = split_nodes_link(after_image_extracted)
        return after_link_extracted
    except Exception as e:
        print(e)

def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:]
    raise Exception("No Header Found!")
   