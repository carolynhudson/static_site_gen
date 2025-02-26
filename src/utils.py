from htmlnode import ParentNode
from textblock import TextBlock
import os
import shutil

def markdown_to_html_node(markdown : str) -> ParentNode:
    return ParentNode("div", [tb.to_htmlnode() for tb in TextBlock.markdown_to_textblock(markdown)])

def list_directory(path : str) -> list[str]:
    return [pathname for name in os.listdir(path) for pathname in ([os.path.join(path, name)] + list_directory(os.path.join(path, name)) if os.path.isdir(os.path.join(path, name)) else [os.path.join(path, name)])]

def copy_folder(source: str, destination: str):

    print(f"Copying from '{source}' to '{destination}':")
    f_copy = 0, f_del = 0, d_make = 0, d_remove = 0

    if not os.path.exists(source):
        raise Exception(f"Source folder or file '{source}' does not exist.")
    
    if os.path.exists(destination):
        if os.path.isdir(destination):
            for dir_item in list_directory(destination)[::-1]:
                if os.path.isdir(dir_item):
                    print(f"Removing destination folder: '{dir_item}'")
                    os.rmdir(dir_item)
                    d_remove += 1
                else:
                    print(f"  Deleteing destination file: '{dir_item}'")
                    os.remove(dir_item)
                    f_del += 1
        else:
            print(f"Deleteing destination file: '{dir_item}'")
            os.remove(destination)
            f_del += 1
    else:
        print(f"Creating destination folder '{destination}'.")
        os.mkdir(destination)
        d_make += 1
    
    if os.path.isfile(source):
        objects_to_copy = [(source, os.path.join(destination, os.path.basename(source)))]
    else:
        objects_to_copy = [(path, os.path.join(destination, path.removeprefix(source).lstrip("/"))) for path in list_directory(source)]
    
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