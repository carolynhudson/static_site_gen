from enum import Enum
from htmlnode import LeafNode
from constants import *
import re

class TextType(Enum):
    NORMAL = "Normal"
    BOLD = "Bold"
    ITALIC = "Italic"
    CODE = "Code"
    LINK = "Link"
    IMAGE = "Image"

class TextNode:
    def __init__(self, text: str, text_type : TextType = TextType.NORMAL, url: str = None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, value ):
        return self.text == value.text and self.text_type == value.text_type and self.url == value.url
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
    
    def to_html_node(self) -> LeafNode:
        match self.text_type:
            case TextType.NORMAL:
                return LeafNode(None, self.text)
            case TextType.BOLD:
                return LeafNode("b", self.text)
            case TextType.ITALIC:
                return LeafNode("i", self.text)
            case TextType.CODE:
                return LeafNode("code", self.text)
            case TextType.LINK:
                return LeafNode("a", self.text, {} if self.url is None or self.url == "" or self.url.isspace() else {"href": self.url})
            case TextType.IMAGE:
                return LeafNode("img", "", dict([(k, v) for k, v in [("src", self.url), ("alt", self.text)] if v is not None and v != "" and not v.isspace()]))
            case _:
                raise Exception("TextNode contains an unsupported TextType.")
            
    def _split_nodes_delimiter(old_nodes: list['TextNode'], delimiter: str, text_type: TextType) -> list['TextNode']:
        if type(old_nodes) is not list:
            raise ValueError("old_nodes must be a list of TextNodes.")
        elif delimiter is None or len(delimiter) == 0:
            raise ValueError("delimiter must be a string of at least one character.")
        elif text_type is None: 
            raise ValueError("text_type must be a valid TextType.")
        
        return [tnode for text, old_type, old_url in [(node.text, node.text_type, node.url) for node in old_nodes] 
                    for tnode in map(lambda enum_tup: TextNode(enum_tup[1], old_type, old_url) if enum_tup[0] % 2 == 0 else TextNode(enum_tup[1], text_type), enumerate(text.split(delimiter))) 
                        if len(tnode.text) > 0]

    def _extract_markdown_ref(text: str, image_ref: bool = False, return_textnodes: bool = False):
        if text is None or type(text) is not str:
                raise ValueError(f"extract_markdown_{"images" if image_ref else "links"} requires a string")
        regex_pattern = MD_IMAGE_EXTRACTION_REGEX if image_ref else MD_LINK_EXTRACTION_REGEX
        pattern = re.compile(regex_pattern)
        if return_textnodes:
            return [TextNode(text, TextType.IMAGE, url) if image_ref else TextNode(text, TextType.LINK, url) for text, url in pattern.findall(text)]
        else:
            return pattern.findall(text)

    def _split_nodes_image(old_nodes : list) -> list['TextNode']:
        if type(old_nodes) is not list:
            raise ValueError("Parameter old_nodes must be a list of TextNodes.")
        regex_pattern = MD_IMAGE_DETECTION_REGEX
        pattern = re.compile(regex_pattern)
        return [tnode for text, old_type, old_url in [(node.text, node.text_type, node.url) for node in old_nodes]
                    for tnode in map(lambda st: TextNode._extract_markdown_ref(st, True, True)[0] if pattern.search(st) != None else TextNode(st, old_type, old_url), [split_text for split_text in pattern.split(text) if len(split_text) > 0])]

    def _split_nodes_link(old_nodes : list) -> list['TextNode']:
        if type(old_nodes) is not list:
            raise ValueError("Parameter old_nodes must be a list of TextNodes.")
        regex_pattern = MD_LINK_DETECTION_REGEX
        pattern = re.compile(regex_pattern)
        return  [tnode for text, old_type, old_url in [(node.text, node.text_type, node.url) for node in old_nodes]
                    for tnode in map(lambda st: TextNode._extract_markdown_ref(st, False, True)[0] if pattern.search(st) != None else TextNode(st, old_type, old_url), [split_text for split_text in pattern.split(text) if len(split_text) > 0])]

    def text_to_textnodes(text: str) -> list['TextNode']: 
        operations = [TextNode._split_nodes_image, 
                    TextNode._split_nodes_link,
                    lambda nodes: TextNode._split_nodes_delimiter(nodes, "**", TextType.BOLD),
                    lambda nodes: TextNode._split_nodes_delimiter(nodes, "__", TextType.BOLD),
                    lambda nodes: TextNode._split_nodes_delimiter(nodes, "*", TextType.ITALIC), 
                    lambda nodes: TextNode._split_nodes_delimiter(nodes, "_", TextType.ITALIC), 
                    lambda nodes: TextNode._split_nodes_delimiter(nodes, "`", TextType.CODE)]
        nodes = [TextNode(text)]
        for func in operations:
            nodes = func(nodes)
        return nodes