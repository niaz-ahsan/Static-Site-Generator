from textnode import TextNode, TextType
from file_moving import copy_static_public, generate_pages_recursive

def main():
    '''
    tnode1 = TextNode("Hello World", TextType.TEXT)
    tnode2 = TextNode("A hyperlink", TextType.LINK, "https://github.com/niaz-ahsan/Static-Site-Generator")

    print(tnode1)
    print(tnode2)
    '''
    # Copying all Static Contents from 'static/' to 'public/' 
    src = "static"
    dest = "public"
    copy_static_public(src, dest)

    # Generate Page
    '''
    src_md_path = "content/index.md"
    html_template_path = "template.html"
    dest_html_path = "public/index.html"
    generate_page(src_md_path, html_template_path, dest_html_path)
    '''
    src_md_content_path = "content"
    dest_html_content_path = "public"
    template_path = "template.html"
    generate_pages_recursive(src_md_content_path, template_path, dest_html_content_path)

main()
