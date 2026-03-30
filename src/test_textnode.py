import unittest

from textnode import TextNode, TextType, text_node_to_html_node

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

# Checking if this file is executed directly
if __name__ == "__main__":
    unittest.main()        