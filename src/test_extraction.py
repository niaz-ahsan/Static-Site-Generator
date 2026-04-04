import unittest
from extraction import extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes, extract_title
from textnode import TextNode, TextType

class TestLinkExtraction(unittest.TestCase):
    def test_md_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)  

    def test_md_images_multiple(self):
        text = "This image ![Some Image](https://something/xom) is okay but this ![another](https://sha/sha)... nice"
        matches = extract_markdown_images(text)
        expected = [
            ("Some Image", "https://something/xom"),
            ("another", "https://sha/sha")
        ]
        self.assertEqual(matches, expected)

    def test_md_images_combined(self):
        text = "This image ![Some Image](https://something/xom) is okay, this is a [hyperlink](https://link/link)"
        matches = extract_markdown_images(text)
        expected = [
            ("Some Image", "https://something/xom")
        ]
        self.assertEqual(matches, expected)

    def test_md_links_multiple(self):
        text = "This is a [hyperlink](https://something/xom) and this [another](https://sha/sha)... nice"
        matches = extract_markdown_links(text)
        expected = [
            ("hyperlink", "https://something/xom"),
            ("another", "https://sha/sha")
        ]
        self.assertEqual(matches, expected)

    def test_md_links_combined(self):
        text = "This image ![Some Image](https://something/xom) is okay, this is a [hyperlink](https://link/link)"
        matches = extract_markdown_links(text)
        expected = [
            ("hyperlink", "https://link/link")
        ]
        self.assertEqual(matches, expected)
        
    def test_md_images_none(self):
        text = "Plain text"
        matches = extract_markdown_images(text)
        expected = []
        self.assertEqual(matches, expected)  

    def test_md_links_none(self):
        text = "Plain text"
        matches = extract_markdown_links(text)
        expected = []
        self.assertEqual(matches, expected)  

    def test_md_images_no_alt_text(self):
        text = "My image ![](http://some/thing.png)"
        matches = extract_markdown_images(text)
        expected = [
            ("", "http://some/thing.png")
        ]
        self.assertEqual(matches, expected) 

    def test_md_links_no_hyperlink_text(self):
        text = "My text [](http://some/thing.text)"
        matches = extract_markdown_links(text)
        expected = [
            ("", "http://some/thing.text")
        ]
        self.assertEqual(matches, expected) 

    def test_md_links_only(self):
        text = "[](http://some/thing.text)"
        matches = extract_markdown_links(text)
        expected = [
            ("", "http://some/thing.text")
        ]
        self.assertEqual(matches, expected) 

    def test_md_images_only(self):
        text = "![](http://some/thing.text)"
        matches = extract_markdown_images(text)
        expected = [
            ("", "http://some/thing.text")
        ]
        self.assertEqual(matches, expected) 

    # Test split node, image
    def test_split_node_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
    
    def test_split_node_image_combo1(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_node_image_combo2(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and that's it",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and that's it", TextType.TEXT)
            ],
            new_nodes,
        )

    def test_split_node_image_combo3(self):
        node = TextNode(
            "This is just plain text",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is just plain text", TextType.TEXT)
            ],
            new_nodes,
        )

    def test_split_node_image_combo4(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png)![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )  

    def test_split_node_image_combo5(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    # Test split node, links
    def test_split_node_links(self):
        node = TextNode(
            "This is text with an [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
    
    def test_split_node_link_combo1(self):
        node = TextNode(
            "[link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_node_link_combo2(self):
        node = TextNode(
            "This is text with an [link](https://i.imgur.com/zjjcJKZ.png) and that's it",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and that's it", TextType.TEXT)
            ],
            new_nodes,
        )

    def test_split_node_link_combo3(self):
        node = TextNode(
            "This is just plain text",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is just plain text", TextType.TEXT)
            ],
            new_nodes,
        )

    def test_split_node_link_combo4(self):
        node = TextNode(
            "[link](https://i.imgur.com/zjjcJKZ.png)[second link](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(
                    "second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )  

    def test_split_node_link_combo5(self):
        node = TextNode(
            "[link](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_both_for_link(self):
        node = TextNode(
            "Here is an ![image](https://example.com) and a [link](https://example.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Here is an ![image](https://example.com) and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://example.com"),
            ],
            new_nodes,
        )
    
    
    # test text_to_textnode(text)
    def test_text_to_textnode(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertEqual(nodes, expected)

    def test_text_to_textnode_combo1(self):
        text = "![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg)[link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertEqual(nodes, expected)

    def test_text_to_textnode_combo2(self):
        text = "Plain Text"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("Plain Text", TextType.TEXT),
        ]
        self.assertEqual(nodes, expected)

    # Test extract_title()
    def test_extract_title(self):
        text1 = """
# Something to consider
`code`
"""
        self.assertEqual(extract_title(text1), "Something to consider")
    

# Checking if this file is executed directly
if __name__ == "__main__":
    unittest.main()  
