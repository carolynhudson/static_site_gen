from utils import *

def main():
    print("hello world")
    purge_contents("./public")
    copy_folder("./static", "./public")
    generate_page("./content/index.md", "./template.html", "./public/index.html")


main()
