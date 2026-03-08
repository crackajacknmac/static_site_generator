from textnode import TextNode, TextType

def main():
	text = "This is some text"
	text_type = TextType.LINK
	url = "https://www.boot.dev"
	print(TextNode(text, text_type, url))

main()
