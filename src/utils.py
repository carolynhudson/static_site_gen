from htmlnode import ParentNode
from textblock import TextBlock
import os
import shutil

def markdown_to_html_node(markdown : str) -> ParentNode:
    return ParentNode("div", [tb.to_htmlnode() for tb in TextBlock.markdown_to_textblock(markdown)])

def list_directory(path : str) -> list[str]:
    return [pathname for name in os.listdir(path) for pathname in ([os.path.join(path, name)] + list_directory(os.path.join(path, name)) if os.path.isdir(os.path.join(path, name)) else [os.path.join(path, name)])]

def purge_contents(path: str):
    if os.path.isdir(path):
        for dir_item in list_directory(path)[::-1]:
            if os.path.isdir(dir_item):
                print(f"Removing folder: '{dir_item}'")
                os.rmdir(dir_item)
            else:
                print(f"  Deleteing file: '{dir_item}'")
                os.remove(dir_item)
    else:
        print(f"Deleteing file: '{path}'")
        os.remove(path)
        
def copy_folder(source: str, destination: str):

    print(f"Copying from '{source}' to '{destination}':")
    f_copy = 0
    f_del = 0
    d_make = 0
    d_remove = 0

    if not os.path.exists(source):
        raise Exception(f"Source folder or file '{source}' does not exist.")
    
    if os.path.exists(destination):
        purge_contents(destination)
    else:
        print(f"Creating destination folder '{destination}'.")
        os.mkdir(destination)
        d_make += 1
    
    if os.path.isfile(source):
        objects_to_copy = [(source, os.path.join(destination, os.path.basename(source)))]
    else:
        objects_to_copy = [(path, os.path.join(destination, path.removeprefix(source).lstrip(os.path.pathsep))) for path in list_directory(source)]
    
    for source_object, destination_object in objects_to_copy:
        if os.path.isfile(source_object):
            print(f"Copying source file from '{source_object}' to destination '{destination_object}'.")
            shutil.copy(source_object, destination_object)
            f_copy += 1

        elif os.path.isdir(source_object) and not os.path.exists(destination_object):
            print(f"Creating destination folder '{destination_object}'.")
            os.mkdir(destination_object)
            d_make += 1
    print(f"{f_copy} files were copied and {d_make} directories were created during the copy.")

def extract_title(markdown : str) -> str:
    title = [line.strip().removeprefix("# ").strip() for line in markdown.splitlines() if line.strip().startswith("# ")]
    if len(title) == 0:
        raise Exception("No title found in given markdown.")
    else:
        return title[0]

def generate_page(from_path : str, template_path : str, dest_path: str):
    print(f"Generating page from '{from_path}' to '{dest_path}' using '{template_path}'.")
    if not os.path.exists(from_path) or not os.path.exists(template_path):
        if os.path.exists(from_path):
            raise FileNotFoundError(f"Could not find template file: '{template_path}'.")
        else:
            raise FileNotFoundError(f"Could not find markdown file: '{from_path}'.")
        
    markdown, template = (open(from_path).read(), open(template_path).read())
    html = markdown_to_html_node(markdown).to_html()
    html = template.replace("{{ Content }}", html).replace("{{ Title }}", extract_title(markdown))
    
    dest_path_list = dest_path.split(os.path.pathsep)
    for i in range(1, len(dest_path_list)):
        dest_sub_path = os.path.join(dest_path_list[:i])
        if not os.path.exists(dest_sub_path):
            os.mkdir(dest_sub_path)
    dest_file = open(dest_path, "w")
    dest_file.write(html)
    dest_file.close()
