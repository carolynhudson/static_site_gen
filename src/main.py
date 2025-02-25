from textnode import TextType, TextNode
from htmlnode import HTMLNode, ParentNode, LeafNode
from textblock import BlockType, TextBlock


def main():
    test =  TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")
    print(test)  
    test_md = """# This is a Test

This is a **markdown** test paragraph.
I am making it to demonstrate blocking.

* Testing Unordered Lists
* Again...
* And again...

```def main():
    test =  TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")
    print(test)
print("hello world")
main()```

## New Ordered List

  1. **First**
  2. *Second*
  3. [Google the Third](https://www.google.com/)

### Quotetastic:

![Make a Pie](https://tenor.com/bRBpB.gif)

>To bake an apple pie from scratch,
>You must first create the universe."""
    print(TextBlock.markdown_to_textblock(test_md))
print("hello world")
main()
