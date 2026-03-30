import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_multiple_values(self):
        node = HTMLNode("p", "Hello World", None, {"title":"A Paragraph", "lang":"Mandarin"})
        self.assertEqual(node.props_to_html(), " title=\"A Paragraph\" lang=\"Mandarin\"")

    def test_props_to_html_single_value(self):
        node = HTMLNode("img", "An Image", None, {"href":"https://google.com/image"})
        self.assertEqual(node.props_to_html(), " href=\"https://google.com/image\"")    

    def test_props_to_html_no_value(self):
        node = HTMLNode("img", "An Image", None, {"href":"https://google.com/image"})
        self.assertEqual(node.props_to_html(), " href=\"https://google.com/image\"")

    # Test Leaf Nodes
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Cat", {"href":"https://link/cat/"})
        self.assertEqual(node.to_html(), "<a href=\"https://link/cat/\">Cat</a>")

    # Test Parent Nodes
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

# Checking if this file is executed directly
if __name__ == "__main__":
    unittest.main()      