import unittest

from textnode import TextNode, TextType, text_node_to_html_node, split_nodes_delimiter

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node1 = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node1, node2)

    def test_neq(self):
        node1 = TextNode("This is a link", TextType.LINK, "https://www.google.com")
        node2 = TextNode("This is a link", TextType.IMAGE, "/image.com")
        self.assertNotEqual(node1, node2)

    def test_edge_case(self):
        node1 = TextNode("My link", TextType.BOLD)
        node2 = TextNode("My link", TextType.BOLD, "www.link.com")
        self.assertNotEqual(node1, node2)

    # Testing the TextNode --> LeafNode Conversion
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_italic(self):
        node = TextNode("This is italic", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is italic")

    def test_code(self):
        node = TextNode("print('hello')", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "print('hello')")

    def test_link(self):
        node = TextNode("Click here", TextType.LINK, "https://www.boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Click here")
        self.assertEqual(html_node.props, {"href": "https://www.boot.dev"})

    def test_invalid_type_raises(self):
        node = TextNode("some text", TextType.TEXT)
        node.text_type = "not_a_real_type"
        with self.assertRaises(Exception):
            text_node_to_html_node(node)

    # Testing split_nodes_delimiter(...)
    def test_split_nodes_delimiter_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected_output = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT)
        ]
        self.assertEqual(new_nodes, expected_output)

    def test_split_nodes_delimiter_bold(self):
        node = TextNode("This is text with a **bold block** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected_output = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bold block", TextType.BOLD),
            TextNode(" word", TextType.TEXT)
        ]
        self.assertEqual(new_nodes, expected_output)

    def test_split_nodes_delimiter_bold_multiple(self):
        node = TextNode("**This** is text with a **bold block** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected_output = [
            TextNode("This", TextType.BOLD),
            TextNode(" is text with a ", TextType.TEXT),
            TextNode("bold block", TextType.BOLD),
            TextNode(" word", TextType.TEXT)
        ]
        self.assertEqual(new_nodes, expected_output)

    def test_split_nodes_delimiter_mixed(self):
        node = TextNode("This has **bold** and _italic_ text", TextType.TEXT)
        bold_split = split_nodes_delimiter([node], "**", TextType.BOLD)
        italic_split = split_nodes_delimiter(bold_split, "_", TextType.ITALIC)
        bold_expected_output = [
            TextNode("This has ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and _italic_ text", TextType.TEXT)
        ]
        italic_expected_output = [
            TextNode("This has ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.TEXT)
        ]
        self.assertEqual(bold_split, bold_expected_output)
        self.assertEqual(italic_split, italic_expected_output)

    def test_split_nodes_delimiter_invalid(self):
        node = TextNode("This has a `unclosed code block", TextType.TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "`", TextType.CODE)

# Checking if this file is executed directly
if __name__ == "__main__":
    unittest.main()        