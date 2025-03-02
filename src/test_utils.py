import unittest

from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode
from utils import *

class TestMarkdown_to_HTML_Node(unittest.TestCase):
    def test_eq(self):
      test1 = """# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item"""
      ans1 = "ParentNode(div, [ParentNode(h1, [LeafNode(This is a heading)]), ParentNode(p, [LeafNode(This is a paragraph of text. It has some ), LeafNode(b, bold), LeafNode( and ), LeafNode(i, italic), LeafNode( words inside of it.)]), ParentNode(ul, [ParentNode(li, [LeafNode(This is the first list item in a list block)]), ParentNode(li, [LeafNode(This is a list item)]), ParentNode(li, [LeafNode(This is another list item)])])])"
      test2 = """# Heading it up!    

   * Pew
   * Pew   
   
   
      """
      ans2 = "ParentNode(div, [ParentNode(h1, [LeafNode(Heading it up!)]), ParentNode(ul, [ParentNode(li, [LeafNode(Pew)]), ParentNode(li, [LeafNode(Pew)])])])"
      test3 = """# This is a Test

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
      ans3 = 'ParentNode(div, [ParentNode(h1, [LeafNode(This is a Test)]), ParentNode(p, [LeafNode(This is a ), LeafNode(b, markdown), LeafNode( test paragraph.), LeafNode(I am making it to demonstrate blocking.)]), ParentNode(ul, [ParentNode(li, [LeafNode(Testing Unordered Lists)]), ParentNode(li, [LeafNode(Again...)]), ParentNode(li, [LeafNode(And again...)])]), ParentNode(code, [LeafNode(def main():\n), LeafNode(    test =  TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")\n), LeafNode(    print(test)\n), LeafNode(print("hello world")\n), LeafNode(main()\n)]), ParentNode(h2, [LeafNode(New Ordered List)]), ParentNode(ol, [ParentNode(li, [LeafNode(b, First)]), ParentNode(li, [LeafNode(i, Second)]), ParentNode(li, [LeafNode(a, Google the Third, href="https://www.google.com/")])]), ParentNode(h3, [LeafNode(Quotetastic:)]), ParentNode(p, [LeafNode(img, src="https://tenor.com/bRBpB.gif" alt="Make a Pie")]), ParentNode(blockquote, [LeafNode(To bake an apple pie from scratch,), LeafNode(You must first create the universe.)])])'

      tests = [(test1, ans1), (test2, ans2), (test3, ans3), ("", "ParentNode(div, [])")]
      for test, ans in tests:
          result = str(markdown_to_html_node(test))
          self.assertEqual(result, ans)

class TestExtract_Title(unittest.TestCase):
    def test_eq(self):
        self.assertEqual(extract_title("\n  \njdfbvjksdeg\n       #    My Title 1"), "My Title 1")
        self.assertEqual(extract_title("\n  \n## Bogus Title\n       #    My Title 2 \njiwehghfweiuy\n"), "My Title 2")
        self.assertEqual(extract_title("\n  \n## Bogus Title\n       #    My Title 3   \n # Trick Title"), "My Title 3")

    def test_err(self):
        self.assertRaises(Exception, extract_title, "\n    \n ## Test")
        self.assertRaises(Exception, extract_title, "")

if __name__ == "__main__":
    
    unittest.main()