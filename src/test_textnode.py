import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
        self.assertEqual(TextNode("", TextType.IMAGE, None), TextNode("", TextType.IMAGE))
        self.assertNotEqual(TextNode("A", TextType.CODE, ""), TextNode("a", TextType.CODE, ""))
        self.assertNotEqual(TextNode("B", TextType.CODE, ""), TextNode("B", TextType.ITALIC, ""))
        self.assertNotEqual(TextNode("C", TextType.CODE), TextNode("C", TextType.CODE, ""))

class TestTN2HNFunc(unittest.TestCase):
    def test_eq(self):
        self.assertEqual(TextNode("TestNorm").to_html_node().to_html(), "TestNorm")
        self.assertEqual(TextNode("TestBold", TextType.BOLD).to_html_node().to_html(), "<b>TestBold</b>")
        self.assertEqual(TextNode("TestItalic", TextType.ITALIC).to_html_node().to_html(), "<i>TestItalic</i>")
        self.assertEqual(TextNode("TestCode", TextType.CODE).to_html_node().to_html(), "<code>TestCode</code>")
        self.assertEqual(TextNode("TestLink1", TextType.LINK, "https://www.google.com").to_html_node().to_html(), '<a href="https://www.google.com">TestLink1</a>')
        self.assertEqual(TextNode("TestLink2", TextType.LINK).to_html_node().to_html(), '<a>TestLink2</a>')
        self.assertEqual(TextNode("TestLink3", TextType.LINK, "").to_html_node().to_html(), '<a>TestLink3</a>')
        self.assertEqual(TextNode("TestImage1", TextType.IMAGE, "https://www.boot.dev/_nuxt/new_boots_profile.DriFHGho.webp").to_html_node().to_html(), '<img src="https://www.boot.dev/_nuxt/new_boots_profile.DriFHGho.webp" alt="TestImage1"></img>')
        self.assertEqual(TextNode("TestImage2", TextType.IMAGE).to_html_node().to_html(), '<img alt="TestImage2"></img>')
        self.assertEqual(TextNode("TestImage3", TextType.IMAGE, "").to_html_node().to_html(), '<img alt="TestImage3"></img>')
        self.assertEqual(TextNode(None, TextType.IMAGE, "https://www.boot.dev/_nuxt/new_boots_profile.DriFHGho.webp").to_html_node().to_html(), '<img src="https://www.boot.dev/_nuxt/new_boots_profile.DriFHGho.webp"></img>')
        self.assertEqual(TextNode("", TextType.IMAGE, "https://www.boot.dev/_nuxt/new_boots_profile.DriFHGho.webp").to_html_node().to_html(), '<img src="https://www.boot.dev/_nuxt/new_boots_profile.DriFHGho.webp"></img>')
        self.assertEqual(TextNode(" ", TextType.IMAGE, "https://www.boot.dev/_nuxt/new_boots_profile.DriFHGho.webp").to_html_node().to_html(), '<img src="https://www.boot.dev/_nuxt/new_boots_profile.DriFHGho.webp"></img>')
        self.assertEqual(TextNode(" ", TextType.IMAGE, " ").to_html_node().to_html(), '<img></img>')

    def test_err(self):
        self.assertRaises(Exception, TextNode(" ", None).to_html_node)

class TestText_to_TextNodes(unittest.TestCase):
    def test_eq(self):
        self.assertEqual(TextNode.text_to_textnodes("This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"), [
            TextNode("This is "),
            TextNode("text", TextType.BOLD),
            TextNode(" with an "),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a "),
            TextNode("code block", TextType.CODE),
            TextNode(" and an "),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a "),
            TextNode("link", TextType.LINK, "https://boot.dev")])
        self.assertEqual(TextNode.text_to_textnodes("This is **text with*** an italic word*` and a code block and an `![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg)[ and a link](https://boot.dev)"),[
            TextNode("This is "),
            TextNode("text with", TextType.BOLD),
            TextNode(" an italic word", TextType.ITALIC),
            TextNode(" and a code block and an ", TextType.CODE),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a link", TextType.LINK, "https://boot.dev")])
        self.assertEqual(TextNode.text_to_textnodes(""), [])

class TestSplitNodesFunc(unittest.TestCase):
    def test_eq(self):
        self.assertEqual(TextNode._split_nodes_delimiter([]," ", TextType.NORMAL), [])
        self.assertEqual(TextNode._split_nodes_delimiter([TextNode("Hello world"), TextNode("how **are** you"), TextNode("**emergency**")],"**", TextType.BOLD), [TextNode("Hello world"), TextNode("how "), TextNode("are", TextType.BOLD), TextNode(" you"), TextNode("emergency", TextType.BOLD)])

    def test_err(self):
        self.assertRaises(ValueError, TextNode._split_nodes_delimiter, None, "a", TextType.LINK)
        self.assertRaises(ValueError, TextNode._split_nodes_delimiter, [], "", TextType.LINK)
        self.assertRaises(ValueError, TextNode._split_nodes_delimiter, [], "b", None)
        
class TestExtractMarkdownFunc(unittest.TestCase):
    def test_image_eq(self):
        self.assertEqual(TextNode._extract_markdown_ref("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)", True), [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")])
        self.assertEqual(TextNode._extract_markdown_ref("This is text with a ![rick roll](i.imgur.com/aKaOqIh.gif) and ![obi wan](i.imgur.com/fJRm4Vk.jpeg)", True), [("rick roll", "i.imgur.com/aKaOqIh.gif"), ("obi wan", "i.imgur.com/fJRm4Vk.jpeg")])
        self.assertEqual(TextNode._extract_markdown_ref("This is text with a ![rick roll](http://i.imgur.com/aKaOqIh.gif) and ![obi wan](http://i.imgur.com/fJRm4Vk.jpeg)", True), [("rick roll", "http://i.imgur.com/aKaOqIh.gif"), ("obi wan", "http://i.imgur.com/fJRm4Vk.jpeg")])
        self.assertEqual(TextNode._extract_markdown_ref("This is text with a ![](ftp://i.imgur.com/aKaOqIh.gif) and ![obi.1](https://i.imgur.com/fJRm4Vk.jpeg)", True), [("", "ftp://i.imgur.com/aKaOqIh.gif"), ("obi.1", "https://i.imgur.com/fJRm4Vk.jpeg")])
        self.assertEqual(TextNode._extract_markdown_ref("", True), [])

    def test_link_eq(self):
        self.assertEqual(TextNode._extract_markdown_ref("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"), [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")])
        self.assertEqual(TextNode._extract_markdown_ref("This is text with a link [to boot dev](www.boot.dev) and [to youtube](www.youtube.com/@bootdotdev)"), [("to boot dev", "www.boot.dev"), ("to youtube", "www.youtube.com/@bootdotdev")])
        self.assertEqual(TextNode._extract_markdown_ref("This is text with a link [to boot dev](http://www.boot.dev) and [to youtube](http://www.youtube.com/@bootdotdev)"), [("to boot dev", "http://www.boot.dev"), ("to youtube", "http://www.youtube.com/@bootdotdev")])
        self.assertEqual(TextNode._extract_markdown_ref("This is text with a link [1](ftp://www.boot.dev) and [123456_youtube](ftp://www.youtube.com/@bootdotdev)"), [("1", "ftp://www.boot.dev"), ("123456_youtube", "ftp://www.youtube.com/@bootdotdev")])
        self.assertEqual(TextNode._extract_markdown_ref(""), [])

    def test_err(self):
        self.assertRaises(ValueError, TextNode._extract_markdown_ref, None)

class TestSplitNodesImage(unittest.TestCase):
    def test_eq(self):
        self.assertEqual(TextNode._split_nodes_image([TextNode("Hello World, "), TextNode("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)")]),
                          [TextNode("Hello World, "), TextNode("This is text with a "), TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"), TextNode(" and "), TextNode("obi wan",TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg")])
        self.assertEqual(TextNode._split_nodes_image([TextNode("Hello World, ", TextType.BOLD), TextNode("This is text with a ![rick roll](i.imgur.com/aKaOqIh.gif) and ![obi wan](i.imgur.com/fJRm4Vk.jpeg)")]), 
                          [TextNode("Hello World, ", TextType.BOLD), TextNode("This is text with a "), TextNode("rick roll", TextType.IMAGE, "i.imgur.com/aKaOqIh.gif"), TextNode(" and "), TextNode("obi wan", TextType.IMAGE, "i.imgur.com/fJRm4Vk.jpeg")])
        self.assertEqual(TextNode._split_nodes_image([TextNode("This is text with a ![rick roll](http://i.imgur.com/aKaOqIh.gif) and ![obi wan](http://i.imgur.com/fJRm4Vk.jpeg)"), TextNode(" Hello World!")]), 
                          [TextNode("This is text with a "), TextNode("rick roll", TextType.IMAGE, "http://i.imgur.com/aKaOqIh.gif"), TextNode(" and "), TextNode("obi wan", TextType.IMAGE, "http://i.imgur.com/fJRm4Vk.jpeg"), TextNode(" Hello World!")])
        self.assertEqual(TextNode._split_nodes_image([TextNode("Hello World, "), TextNode("This is text with a ![](ftp://i.imgur.com/aKaOqIh.gif) and ![obi.1](https://i.imgur.com/fJRm4Vk.jpeg)")]), 
                          [TextNode("Hello World, "), TextNode("This is text with a "), TextNode("", TextType.IMAGE, "ftp://i.imgur.com/aKaOqIh.gif"), TextNode(" and "), TextNode("obi.1", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg")])
        self.assertEqual(TextNode._split_nodes_image([TextNode("")]), [])

    def test_err(self):
        self.assertRaises(ValueError, TextNode._split_nodes_image, None)

class TestSplitNodesLink(unittest.TestCase):
    def test_eq(self):
        self.assertEqual(TextNode._split_nodes_link([TextNode("Hello World, "), TextNode("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)")]), 
                          [TextNode("Hello World, "), TextNode("This is text with a link "), TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"), TextNode(" and "), TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev")])
        self.assertEqual(TextNode._split_nodes_link([TextNode("Hello World, ", TextType.BOLD), TextNode("This is text with a link [to boot dev](www.boot.dev) and [to youtube](www.youtube.com/@bootdotdev)")]), 
                          [TextNode("Hello World, ", TextType.BOLD), TextNode("This is text with a link "), TextNode("to boot dev", TextType.LINK, "www.boot.dev"), TextNode(" and "), TextNode("to youtube", TextType.LINK, "www.youtube.com/@bootdotdev")])
        self.assertEqual(TextNode._split_nodes_link([TextNode("This is text with a link [to boot dev](http://www.boot.dev) and [to youtube](http://www.youtube.com/@bootdotdev)"), TextNode(" Hello World!")]), 
                          [TextNode("This is text with a link "), TextNode("to boot dev", TextType.LINK, "http://www.boot.dev"), TextNode(" and "), TextNode("to youtube", TextType.LINK, "http://www.youtube.com/@bootdotdev"), TextNode(" Hello World!")])
        self.assertEqual(TextNode._split_nodes_link([TextNode("Hello World, "), TextNode("This is text with a link [1](ftp://www.boot.dev) and [123456_youtube](ftp://www.youtube.com/@bootdotdev)")]), 
                          [TextNode("Hello World, "), TextNode("This is text with a link "), TextNode("1", TextType.LINK, "ftp://www.boot.dev"), TextNode(" and "), TextNode("123456_youtube", TextType.LINK, "ftp://www.youtube.com/@bootdotdev")])
        self.assertEqual(TextNode._split_nodes_link([TextNode("")]), [])


if __name__ == "__main__":
    unittest.main()