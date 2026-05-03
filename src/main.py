import os
import shutil
from pathlib import Path
from copystatic import generator, extract_title, generate_page, generate_pages_recursive

def main():

    if os.path.exists("public"):
        shutil.rmtree("public")
    os.mkdir("public")
    generator("static", "public")
    generate_pages_recursive("content", "template.html", "public")

main()
