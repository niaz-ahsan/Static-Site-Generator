import unittest

from block_helper import is_heading, is_code_block, is_quote, is_olist

class TestBlockHelper(unittest.TestCase):
    def test_is_heading_True(self):
        data1 = "# Abcc #"
        data2 = "## 1sj $"
        data3 = "### 1234"
        data4 = "#### AAXXZZ"
        data5 = "##### <>><"
        data6 = "###### S"
        self.assertEqual(is_heading(data1), True)
        self.assertEqual(is_heading(data2), True)
        self.assertEqual(is_heading(data3), True)
        self.assertEqual(is_heading(data4), True)
        self.assertEqual(is_heading(data5), True)
        self.assertEqual(is_heading(data6), True)

    def test_is_heading_False(self):
        data1 = "#Abcc #"
        data2 = "##1sj $"
        data3 = "###1234"
        data4 = "####AAXXZZ"
        data5 = "#####<>><"
        data6 = "##########S"
        self.assertEqual(is_heading(data1), False)
        self.assertEqual(is_heading(data2), False)
        self.assertEqual(is_heading(data3), False)
        self.assertEqual(is_heading(data4), False)
        self.assertEqual(is_heading(data5), False)
        self.assertEqual(is_heading(data6), False)

    def test_code_block(self):
        data1 = """```
        Hello World
        ```"""
        data2 = "```Hello World```"
        data3 = "`No"
        self.assertEqual(is_code_block(data1), True)
        self.assertEqual(is_code_block(data2), False)
        self.assertEqual(is_code_block(data3), False)

    def test_quote(self):
        text = """
> Yeah
> Nope
"""
        text2 = """>Some\n>thing"""
        text3 = """
>> Hmm
> No
"""
        self.assertEqual(is_quote(text), True)
        self.assertEqual(is_quote(text2), True)
        self.assertEqual(is_quote(text3), True)

    def test_olist(self):
        text = "1. Yoo" \
        "2. Noo"
        text2 = "1.Nope" \
        "2. Yep"
        self.assertEqual(is_olist(text), True)
        self.assertEqual(is_olist(text2), False)


# Checking if this file is executed directly
if __name__ == "__main__":
    unittest.main() 
