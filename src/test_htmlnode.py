import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        self.assertEqual(str(HTMLNode()), str(HTMLNode(None, None, None, None)))
        self.assertEqual('href="https://www.google.com" target="_blank"', HTMLNode("","",[], {"href": "https://www.google.com", "target": "_blank"}).props_to_html())
        self.assertEqual("", HTMLNode("","",[], {}).props_to_html())
        self.assertEqual('HTMLNode(tag, value, [HTMLNode()], A="a" B="b" C="c")', str(HTMLNode("tag", "value", [HTMLNode()], {"A": "a", "B": "b", "C": "c"})))

class TestLeafNode(unittest.TestCase):
    def test_eq(self):
        self.assertEqual(LeafNode("p", "This is a paragraph of text.").to_html(),"<p>This is a paragraph of text.</p>")
        self.assertEqual(LeafNode("a", "Click me!", {"href": "https://www.google.com"}).to_html(),'<a href="https://www.google.com">Click me!</a>')
        self.assertEqual(LeafNode("", "Just plain text.", {"ignore": "me"}).to_html(),'Just plain text.')
        self.assertEqual(LeafNode(None, "Just plain text.").to_html(),'Just plain text.')
        self.assertEqual(LeafNode(" ", "Just plain text.").to_html(),'Just plain text.')

    def test_err(self):
        self.assertRaises(ValueError, LeafNode("a", None).to_html)


class TestParentfNode(unittest.TestCase):
    def test_eq(self):
        test_node1 = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text")
            ])
        test_node2 = ParentNode(
            "span",
            [   
                ParentNode("p",
                           [
                                LeafNode("b", "L2-1 Bold text"),
                                LeafNode(None, "L2-1 Normal text")                               
                           ]),
                ParentNode("p",
                           [
                                LeafNode("b", "L2-2 Bold text"),
                                LeafNode(None, "L2-2 Normal text")                               
                           ]),
                LeafNode(None, "L1-1 Normal text"),
                LeafNode("i", "L1-2 italic text")
            ], {"href": "https://www.google.com"})
        self.assertEqual(test_node1.to_html(), "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")
        self.assertEqual(test_node2.to_html(), '<span href="https://www.google.com"><p><b>L2-1 Bold text</b>L2-1 Normal text</p><p><b>L2-2 Bold text</b>L2-2 Normal text</p>L1-1 Normal text<i>L1-2 italic text</i></span>')
        self.assertEqual(str(ParentNode("p", [LeafNode(None, "My Text")])), "ParentNode(p, [LeafNode(My Text)])")


    def test_err(self):
        self.assertRaises(ValueError, ParentNode(None, [LeafNode(None , "Just plain text.")]).to_html)
        self.assertRaises(ValueError, ParentNode("", [LeafNode(" ", "Just plain text.")]).to_html)
        self.assertRaises(ValueError, ParentNode("", []).to_html)
        self.assertRaises(ValueError, ParentNode("", None).to_html)
        self.assertRaises(ValueError, ParentNode("", "").to_html)

if __name__ == "__main__":
    unittest.main()