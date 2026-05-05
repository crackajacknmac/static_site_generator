import os
import shutil
import sys
from pathlib import Path
from copystatic import generator, extract_title, generate_page, generate_pages_recursive

def main():
    basepath = "/"
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    if os.path.exists("docs"):
        shutil.rmtree("docs")
    os.mkdir("docs")
    generator("static", "docs")
    generate_pages_recursive("content", "template.html", "docs", basepath)

main()
