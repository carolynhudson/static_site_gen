from utils import *
from constants import *
import sys

def main():
    base_path = "/" if len(sys.argv) <= 1 else sys.argv[1]
    print(f"Static site generation web server base path: '{base_path}'")
    purge_contents(SITE_ROOT_FOLDER)
    copy_folder(STATIC_CONTENT_FOLDER, SITE_ROOT_FOLDER)
    generate_pages_recursive(MARKDOWN_CONTENT_FOLDER, "./template.html", SITE_ROOT_FOLDER, base_path)

main()
