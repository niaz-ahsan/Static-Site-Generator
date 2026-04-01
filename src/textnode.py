from enum import Enum
from htmlnode import LeafNode

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return self.text == other.text and \
        self.text_type == other.text_type and \
        self.url == other.url
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
    

def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.TEXT:
        return LeafNode(None, text_node.text)
    elif text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)
    elif text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)
    elif text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)
    elif text_node.text_type == TextType.LINK:
        return LeafNode("a", text_node.text, {"href":text_node.url})
    elif text_node.text_type == TextType.IMAGE:
        props = {
            "src": text_node.url,
            "alt": text_node.text
        }
        return LeafNode("img", "", props)
    else:
        raise Exception("Type not supported!")

# old_nodes: a list of TextNodes
# delimiter: by which delim we should split
# text_type: after split type of text found in the odd index, 
# all even index item will be of TextType.TEXT        
def split_nodes_delimiter(old_nodes, delimeter, text_type):
    output = []
    for node in old_nodes:
        # anything other than TEXT should be added as is
        if node.text_type != TextType.TEXT:
            output.append(node)
            continue
        parts = node.text.split(delimeter)
        # checking closing delimeter, even # parts --> exists unclosed delim
        if len(parts) % 2 == 0:
            raise Exception("Invalid Markdown Syntax!")
        for i, part in enumerate(parts):
            if len(part) > 0:
                part_text_type = TextType.TEXT if i % 2 == 0 else text_type 
                output.append(TextNode(part, part_text_type))
    return output

     

    

