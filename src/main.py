from textnode import TextNode, TextType

def main():
    tnode1 = TextNode("Hello World", TextType.TEXT)
    tnode2 = TextNode("A hyperlink", TextType.LINK, "https://github.com/niaz-ahsan/Static-Site-Generator")

    print(tnode1)
    print(tnode2)

main()
