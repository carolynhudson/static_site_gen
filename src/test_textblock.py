import unittest

from textblock import BlockType, TextBlock
from htmlnode import ParentNode, LeafNode

class TestMD_to_Blocks(unittest.TestCase):
    def test_eq(self):
        test1 = """# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item"""
        ans1 = ['# This is a heading', 'This is a paragraph of text. It has some **bold** and *italic* words inside of it.', '* This is the first list item in a list block\n* This is a list item\n* This is another list item']
        test2 = """# Heading it up!    

   * Pew
   * Pew   
   
   
      """
        ans2 = ['# Heading it up!', '* Pew\n* Pew']
        tests = [(test1, ans1), (test2, ans2), ("    \n\n    \n\n\n", [])]
        for test, ans in tests:
            self.assertEqual(TextBlock._markdown_to_blocks(test), ans)


class TestTextBlock(unittest.TestCase):
    def test_eq(self):
        self.assertEqual(TextBlock._text_to_block_type("* Test\n* Testing\n* Testing 123"), BlockType.UNORDERED_LIST)
        self.assertEqual(TextBlock._text_to_block_type("- Test\n- Testing\n- Testing 123"), BlockType.UNORDERED_LIST)
        self.assertEqual(TextBlock._text_to_block_type("- Test\n- Testing\n Testing 123"), BlockType.PARAGRAPH)
        self.assertEqual(TextBlock._text_to_block_type("1. Test\n2. Testing\n3. Testing 123"), BlockType.ORDERED_LIST)
        self.assertEqual(TextBlock._text_to_block_type("Test\n1. Testing\n2. Testing 123"), BlockType.PARAGRAPH)
        self.assertEqual(TextBlock._text_to_block_type("###### Test"), BlockType.HEADING)
        self.assertEqual(TextBlock._text_to_block_type('``` for i in range(10):\nprint("hello")\nprint(i)```'), BlockType.CODE)
        self.assertEqual(TextBlock._text_to_block_type("> Test\n> Testing\n> Testing 123"), BlockType.QUOTE)

class TestMD_to_TextBlock(unittest.TestCase):
    def test_eq(self):
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
        test_ans = [TextBlock("This is a Test", BlockType.HEADING, "#"),
                    TextBlock("This is a **markdown** test paragraph.\nI am making it to demonstrate blocking.", BlockType.PARAGRAPH),
                    TextBlock("Testing Unordered Lists\nAgain...\nAnd again...", BlockType.UNORDERED_LIST, "*"),
                    TextBlock('def main():\n    test =  TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")\n    print(test)\nprint("hello world")\nmain()', BlockType.CODE),
                    TextBlock("New Ordered List", BlockType.HEADING, "##"), 
                    TextBlock("**First**\n*Second*\n[Google the Third](https://www.google.com/)", BlockType.ORDERED_LIST),
                    TextBlock("Quotetastic:", BlockType.HEADING, "###"),
                    TextBlock("![Make a Pie](https://tenor.com/bRBpB.gif)", BlockType.PARAGRAPH),
                    TextBlock("To bake an apple pie from scratch,\nYou must first create the universe.", BlockType.QUOTE)]
        self.assertEqual(TextBlock.markdown_to_textblock(test_md), test_ans)
        self.assertEqual(TextBlock.markdown_to_textblock(""), [])

class Test_to_HTMLNode(unittest.TestCase):
    def test_eq(self):
        self.assertEqual(str(TextBlock("Heading", BlockType.HEADING, "##").to_htmlnode()), str(ParentNode("h2",[LeafNode("", "Heading")])))
        self.assertEqual(str(TextBlock("Paragraph", BlockType.PARAGRAPH).to_htmlnode()), str(ParentNode("p",[LeafNode("", "Paragraph")])))
        self.assertEqual(str(TextBlock("Code", BlockType.CODE).to_htmlnode()), str(ParentNode("code",[LeafNode("", "Code\n")])))
        self.assertEqual(str(TextBlock("Quote", BlockType.QUOTE).to_htmlnode()), str(ParentNode("blockquote",[LeafNode("", "Quote")])))
        self.assertEqual(str(TextBlock("Ordered List", BlockType.ORDERED_LIST).to_htmlnode()), str(ParentNode("ol",[ParentNode("li",[LeafNode("", "Ordered List")])])))
        self.assertEqual(str(TextBlock("Unordered List", BlockType.UNORDERED_LIST, "*").to_htmlnode()), str(ParentNode("ul",[ParentNode("li",[LeafNode("", "Unordered List")])])))

if __name__ == "__main__":
    unittest.main()