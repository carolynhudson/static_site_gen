from htmlnode import ParentNode
from textblock import TextBlock

def markdown_to_html_node(markdown : str) -> ParentNode:
    return ParentNode("div", [tb.to_htmlnode() for tb in TextBlock.markdown_to_textblock(markdown)])
