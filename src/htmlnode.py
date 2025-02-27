class HTMLNode():

    def __init__(self, tag : str = None, value: str = None, children : list = None, props : dict = None) :
        self.tag = tag #- A string representing the HTML tag name (e.g. "p", "a", "h1", etc.)
        self.value = value #- A string representing the value of the HTML tag (e.g. the text inside a paragraph)
        self.children = children#- A list of HTMLNode objects representing the children of this node
        self.props = props #- A dictionary of key-value pairs representing the attributes of the HTML tag. For example, a link (<a> tag) might have {"href": "https://www.google.com"}

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self) -> str: 
        return " ".join([f'{key}="{value}"' for key, value in self.props.items()]) if self.props != None else ""
    
    def __eq__(self, value : 'HTMLNode'):
        return self.tag == value.tag and self.value == value.value and self.children == value.children and self.props == value.props
    
    def __repr__(self) -> str:
        return f"{type(self).__name__}({", ".join([str(v) for v in [self.tag, self.value, self.children, self.props_to_html()] if v != None and v != ""])})"
    
class LeafNode(HTMLNode):
    def __init__(self, tag: str, value: str, props: dict = None):
        super().__init__(tag, value, None, props)
    
    def to_html(self) -> str:
        if self.value is None:
            raise ValueError("A LeafNode must have a value.")
        else:
            return self.value if self.tag is None or self.tag == "" or self.tag.isspace() else f'<{" ".join([v for v in [self.tag, self.props_to_html()] if v != ""])}>{self.value}</{self.tag}>'

class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: list, props: dict = None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None or self.tag == "" or self.tag.isspace():
            raise ValueError("A ParentNode must contain have a tag.")
        elif self.children is None or type(self.children) is not list or len(self.children) == 0:
            print(self)
            raise ValueError("A ParentNode must have a children list containing of at least one child node.")
        else:
            return f'<{" ".join([v for v in [self.tag, self.props_to_html()] if v != ""])}>{"".join([c.to_html() for c in self.children])}</{self.tag}>\n'