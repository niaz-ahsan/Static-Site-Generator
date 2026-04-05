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

# No longer used
def generate_page(from_path, template_path, dest_path, basepath):
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
    template_content = template_content.replace("href=\"/", f"href=\"{basepath}")
    template_content = template_content.replace("src=\"/", f"src=\"{basepath}")
    ###### find dest dir by ommitting file name ####
    small_pcs = dest_path.split("/")
    dest_dir = "/".join(small_pcs[:-1])
    os.makedirs(dest_dir, exist_ok = True)
    with open(dest_path, "w") as file:
        file.write(template_content)    

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    filenames = os.listdir(dir_path_content)
    for filename in filenames:
        filepath = f"{dir_path_content}/{filename}"
        if os.path.isfile(filepath):
            # read the file contents
            file_md_content = get_file_content(filepath)
            # read the template content
            template_content = get_file_content(template_path)
            # convert file content to HTML
            converted_html_content = convert_md_html_file(file_md_content, template_content, basepath)
            # write HTML content to respective dest dir
            write_html_content_to_output_file(converted_html_content, dest_dir_path, filename)
        else:
            # this is a sub-dir
            # recustively call the func
            new_dest_dir_path = f"{dest_dir_path}/{filename}"
            generate_pages_recursive(filepath, template_path, new_dest_dir_path, basepath)

def get_file_content(filepath):
    output = ""
    with open(filepath, "r") as file:
        output = file.read()
    return output

def convert_md_html_file(file_md_content, template_content, basepath):
    html_node = markdown_to_html_node(file_md_content)
    html_content = html_node.to_html()
    page_title = extract_title(file_md_content)
    template_content = template_content.replace("{{ Title }}", page_title)
    template_content = template_content.replace("{{ Content }}", html_content) 
    template_content = template_content.replace("href=\"/", f"href=\"{basepath}")
    template_content = template_content.replace("src=\"/", f"src=\"{basepath}")
    return template_content

def write_html_content_to_output_file(html_content, dest_dir, dest_filename):
    os.makedirs(dest_dir, exist_ok=True)
    filename = dest_filename.split(".")[0]
    dest_path = f"{dest_dir}/{filename}.html"
    with open(dest_path, "w") as file:
        file.write(html_content)