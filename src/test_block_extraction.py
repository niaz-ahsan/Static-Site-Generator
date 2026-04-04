import unittest
from block_extraction import markdown_to_blocks, block_to_block_type, BlockType

class TestBlockExtraction(unittest.TestCase):
    def test_md_to_block(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_md_to_block_combo(self):
        md = """
This is **bolded** paragraph



Oh Yeah
Hiua hiya
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "Oh Yeah\nHiua hiya",
            ],
        )   

    def test_block_type(self):
        text1 = "## Hello World"
        text2 = "```\nsome code here\n```" 
        text3 = "> This is a quote\n> Another line"
        text4 = "- item one\n- item two\n- item three"
        text5 = "1. first\n2. second\n3. third"
        text6 = "Just some regular text."
        self.assertEqual(block_to_block_type(text1), BlockType.HEADING)
        self.assertEqual(block_to_block_type(text2), BlockType.CODE)
        self.assertEqual(block_to_block_type(text3), BlockType.QUOTE)
        self.assertEqual(block_to_block_type(text4), BlockType.ULIST)
        self.assertEqual(block_to_block_type(text5), BlockType.OLIST)
        self.assertEqual(block_to_block_type(text6), BlockType.PARAGRAPH)
        

# Checking if this file is executed directly
if __name__ == "__main__":
    unittest.main() 
