from utils import *
from constants import *

def main():
    print("hello world")

    purge_contents(SITE_ROOT_FOLDER)
    copy_folder(STATIC_CONTENT_FOLDER, SITE_ROOT_FOLDER)
    generate_pages_recursive(MARKDOWN_CONTENT_FOLDER, "./template.html", SITE_ROOT_FOLDER)

main()
