import os
import shutil
from md_to_html_node import markdown_to_html_node
from extraction import extract_title

def delete_contents(path):
    # Check if dir exists and remove all content from it.
    if os.path.exists(path) and os.path.isdir(path):
        shutil.rmtree(path) # recursively deletes dir content

# see if dir exists, if not - create. 
# If exists empty dir
def check_dest_dir(path):
    if os.path.exists(path):
        delete_contents(path)
    os.mkdir(path)
    
def copy_contents(src_path, dest_path):
    if os.path.exists(src_path):
        contents = os.listdir(src_path)
        for item in contents:
            # if this is a file, copy it to dest
            filepath = f"{src_path}/{item}"
            if os.path.isfile(filepath):
                shutil.copy(filepath, dest_path)
            elif os.path.isdir(filepath):
                new_dest_path = f"{dest_path}/{item}"
                os.mkdir(new_dest_path)
                copy_contents(filepath, new_dest_path)
    

def copy_static_public(src_path, dest_path):
    check_dest_dir(dest_path)
    copy_contents(src_path, dest_path)


####################################################################

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    md_content = ""
    template_content = ""
    with open(from_path, "r") as file:
        md_content = file.read()
    with open(template_path, "r") as file:
        template_content = file.read()
    html_node = markdown_to_html_node(md_content)
    html_content = html_node.to_html()
    page_title = extract_title(md_content)
    template_content = template_content.replace("{{ Title }}", page_title)
    template_content = template_content.replace("{{ Content }}", html_content)  
    ###### find dest dir by ommitting file name ####
    small_pcs = dest_path.split("/")
    dest_dir = "/".join(small_pcs[:-1])
    os.makedirs(dest_dir, exist_ok = True)
    with open(dest_path, "w") as file:
        file.write(template_content)    