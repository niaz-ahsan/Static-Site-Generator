import sys
from textnode import TextNode, TextType
from file_moving import copy_static_public, generate_pages_recursive

def main():
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"

    # Copying all Static Contents from 'static/' to 'docs/' 
    src = "static"
    dest = "docs"
    copy_static_public(src, dest)

    # Generate Page
    src_md_content_path = "content"
    dest_html_content_path = "docs"
    template_path = "template.html"
    generate_pages_recursive(src_md_content_path, template_path, dest_html_content_path, basepath)

main()
