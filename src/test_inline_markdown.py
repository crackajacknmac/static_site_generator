import unittest
from textnode import TextType, TextNode
from inline_markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes

class TestInline(unittest.TestCase):
    def test_normal_output(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
        new_nodes,
        [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT)
        ],
    )

    def test_flawed_output(self):
        node = TextNode("This is some **plain text", TextType.TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "**", TextType.BOLD)

    def test_bold(self):
        node = TextNode("To **boldly** go where no man has gone before!", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
        new_nodes,
        [
            TextNode("To ", TextType.TEXT),
            TextNode("boldly", TextType.BOLD),
            TextNode(" go where no man has gone before!", TextType.TEXT)
        ],
    )

    def test_extract_images(self):
        matches = extract_markdown_images(
            "Some of the worst tragedies in history have been followed with ![image](https://www.Iwasjustfollowingorders.com)"
        )
        self.assertListEqual([("image", "https://www.Iwasjustfollowingorders.com")], matches)

    def test_extract_links(self):
        matches = extract_markdown_links(
            "You may test that assumption [at your convenience](https://www.Picardquotes.com)"
        )
        self.assertListEqual([("at your convenience", "https://www.Picardquotes.com")], matches)



    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is some text with a [link](https://www.serebii.com) and another [link](https://www.wow.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is some text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.serebii.com"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.wow.com"
                ),
            ],
            new_nodes,
        )

    def test_no_images(self):
        node = TextNode(
            "Space. The final frontier. These are the voyages of the starship, Enterprise.",
            TextType.TEXT,
            )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("Space. The final frontier. These are the voyages of the starship, Enterprise.", TextType.TEXT
                ),
            ],
            new_nodes,
        )

    def test_no_links(self):
        node = TextNode(
            "To explore strange new worlds and seek out new life and civilizations.",
            TextType.TEXT,
            )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("To explore strange new worlds and seek out new life and civilizations.", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_link_end(self):
        node = TextNode(
            "To the red crown of [Omadon](https://www.flightofdragons.com)",
            TextType.TEXT,
            )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("To the red crown of ", TextType.TEXT),
                TextNode("Omadon", TextType.LINK, "https://www.flightofdragons.com"),
            ],
            new_nodes,
        )


    def test_image_end(self):
        node = TextNode(
            "Away with your millwheel. I call upon all the blue magic to make it disappear! ![greenmage](https://www.flightofdragons.com)",
            TextType.TEXT,
            )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("Away with your millwheel. I call upon all the blue magic to make it disappear! ", TextType.TEXT),
                TextNode("greenmage", TextType.IMAGE, "https://www.flightofdragons.com"),
            ],
            new_nodes,
        )

    def test_image_start(self):
        node = TextNode(
            "![PeterDickenson](https://www.flightofdragons.com) You are unique.",
            TextType.TEXT,
            )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("PeterDickenson", TextType.IMAGE, "https://www.flightofdragons.com"),
                TextNode(" You are unique.", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_link_start(self):
        node = TextNode(
            "[Omadon](https://www.flightofdragons.com)Greed and avarice shall prevail. And those who do not heed my words shall pay the price.",
            TextType.TEXT,
            )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Omadon", TextType.LINK, "https://www.flightofdragons.com"),
                TextNode("Greed and avarice shall prevail. And those who do not heed my words shall pay the price.", TextType.TEXT),
            ],
            new_nodes,
        )


    def test_multiple_images(self):
        node = TextNode(
            "I'll teach man what to do with his machines. ![deforester](https://www.Ferngully.com)I'll teach man how to fly like a fairy.![doom](https://www.flightofdragons.com)",
            TextType.TEXT,
            )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("I'll teach man what to do with his machines. ", TextType.TEXT),
                TextNode("deforester", TextType.IMAGE, "https://www.Ferngully.com"),
                TextNode("I'll teach man how to fly like a fairy.", TextType.TEXT),
                TextNode("doom", TextType.IMAGE, "https://www.flightofdragons.com"),
            ],
            new_nodes,
        )

    def test_multiple_links(self):
        node = TextNode(
            "[nuke](https://www.doom.com)And the world will be free for my magic again.[completepsycho](https://www.totheredcrownofomadon.com)",
            TextType.TEXT,
            )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("nuke", TextType.LINK, "https://www.doom.com"),
                TextNode("And the world will be free for my magic again.", TextType.TEXT),
                TextNode("completepsycho", TextType.LINK, "https://www.totheredcrownofomadon.com"),
            ],
            new_nodes,
        )


    def test_inline_markdown_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ]
        )


if __name__=="__main__":
    unittest.main()
