import os
import shutil
from textnode import TextNode, TextType
from copystatic import generator

def main():
    '''text = "This is some text"
    text_type = TextType.LINK
    url = "https://www.boot.dev"
    print(TextNode(text, text_type, url))'''

    if os.path.exists("public"):
        shutil.rmtree("public")
    os.mkdir("public")
    generator("static", "public")

main()
