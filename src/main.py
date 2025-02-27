from utils import *
from constants import *

def main():
    print("hello world")

    purge_contents(SITE_ROOT_FOLDER)
    copy_folder(STATIC_CONTENT_FOLDER, SITE_ROOT_FOLDER)
    for page_to_generate in [(content, "./template.html", SITE_ROOT_FOLDER + content.removeprefix(MARKDOWN_CONTENT_FOLDER).removesuffix(".md") + ".html") for content in list_directory(MARKDOWN_CONTENT_FOLDER) if content.endswith(".md")]:
        generate_page(*page_to_generate)


main()
