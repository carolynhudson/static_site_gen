from enum import Enum
from constants import *
from textnode import TextType, TextNode
from htmlnode import LeafNode, ParentNode
import re
import inspect

class BlockType(Enum):
    PARAGRAPH = "Paragraph"
    HEADING = "Heading"
    CODE = "Code"
    QUOTE = "Quote"
    UNORDERED_LIST = "Unordered_List"
    ORDERED_LIST = "Ordered_List"

class TextBlock:
    def __init__(self, text: str, block_type : BlockType = BlockType.PARAGRAPH, block_style : str = None):
        self.text = text
        self.block_type = block_type
        self.block_style = block_style
        self.__text_nodes = [[TextNode(line)] if block_type == BlockType.CODE else TextNode.text_to_textnodes(line) for line in text.splitlines(True)]

    def __eq__(self, value : 'TextBlock') -> bool:
        return self.text == value.text and self.block_type == value.block_type and self.block_style == value.block_style
    
    def __repr__(self) -> str:
        return f"TextBlock({self.block_type.value}, {self.block_style}, {self.text})"
    
    def to_htmlnode(self) -> ParentNode:
        match self.block_type:
            case BlockType.PARAGRAPH:
                return ParentNode("p", [node.to_html_node() for line_nodes in self.__text_nodes for node in line_nodes])
            case BlockType.QUOTE:
                return ParentNode("blockquote", [node.to_html_node() for line_nodes in self.__text_nodes for node in line_nodes])
            case BlockType.CODE:
                return ParentNode("code", [node.to_html_node() for line_nodes in self.__text_nodes for node in line_nodes])
            case BlockType.HEADING:
                return ParentNode(f"h{len(self.block_style)}", [node.to_html_node() for line_nodes in self.__text_nodes for node in line_nodes])
            case BlockType.UNORDERED_LIST:
                return ParentNode("ul", [ParentNode("li", [node.to_html_node() for node in line_nodes]) for line_nodes in self.__text_nodes])
            case BlockType.ORDERED_LIST:
                return ParentNode("ol", [ParentNode("li", [node.to_html_node() for node in line_nodes]) for line_nodes in self.__text_nodes])

    
    def _markdown_to_blocks(markdown : str) -> list[str]: 
        pattern = re.compile(MD_BLOCK_SPLITTER, re.MULTILINE)
        return [block.strip() for block in pattern.split("\n".join([line.strip() for line in markdown.splitlines()])) if len(str.strip(block)) > 0]

    def _text_to_block_type(text : str) -> BlockType:
        pattern = re.compile(BLOCKTYPE_IDENTIFIER, re.MULTILINE + re.DOTALL)
        block_tuples = [([BlockType(key) for key, value in match.groupdict().items() if value is not None][0], match[0].rstrip(". ")) if len(set(match.groupdict().values())) > 1 else ("Paragraph", "") for match in pattern.finditer(text)]
        block_type = block_tuples[0][0]
        match block_type:
            case BlockType.QUOTE:
                return BlockType.QUOTE if all([line_type == BlockType.QUOTE for line_type, match_str in block_tuples]) else BlockType.PARAGRAPH
            case BlockType.UNORDERED_LIST:
                return BlockType.UNORDERED_LIST if all([line_type == BlockType.UNORDERED_LIST for line_type, match_str in block_tuples]) else BlockType.PARAGRAPH
            case BlockType.ORDERED_LIST:
                return BlockType.ORDERED_LIST if [match_str for line_type, match_str in block_tuples] == [str(ln) for ln in range(1, len(block_tuples) + 1)] else BlockType.PARAGRAPH
            case _:
                return block_type
            
    def markdown_to_textblock(markdown : str) -> list['TextBlock']:
        cleaner_re_dict = {BlockType(type_val): (re.compile(regex, re.MULTILINE) if len(regex) > 0 else None) for type_val, regex in BLOCKTYPE_CLEANERS}
        cleaner = lambda block_type, text: text if cleaner_re_dict[block_type] is None else cleaner_re_dict[block_type].sub("", text) 

        get_style_re_dict = {BlockType(type_val): (re.compile(regex, re.MULTILINE) if len(regex) > 0 else None) for type_val, regex in BLOCKTYPE_GET_STYLE}
        get_style = lambda block_type, text: (None if get_style_re_dict[block_type] is None else get_style_re_dict[block_type].search(text)[1])

        return [TextBlock(cleaner(block_type, text), block_type, get_style(block_type, text)) for text, block_type in [(text, TextBlock._text_to_block_type(text)) for text in TextBlock._markdown_to_blocks(markdown)]]
    


                