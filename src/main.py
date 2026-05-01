import os
import shutil
from copystatic import generator, extract_title, generate_page

def main():

    if os.path.exists("public"):
        shutil.rmtree("public")
    os.mkdir("public")
    generator("static", "public")
    generate_page("content/index.md", "template.html", "public/index.html")

main()
