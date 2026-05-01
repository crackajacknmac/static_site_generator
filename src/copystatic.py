import os
import shutil
from markdown_blocks import block_to_block_type, markdown_to_blocks, markdown_to_html_node
from htmlnode import HTMLNode

def generator(static, public):
    if not os.path.exists(public):
        os.mkdir(public)
    static_list = os.listdir(static)
    for name in static_list:
        static_file_path = os.path.join(static, name)
        public_file_path = os.path.join(public, name)
        if os.path.isfile(static_file_path):
            shutil.copy(static_file_path, public_file_path)
        if os.path.isdir(static_file_path):
            os.mkdir(public_file_path)
            generator(static_file_path, public_file_path)

def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            title = line[2:]
            title = title.rstrip()
            return title
    raise Exception("no heading found")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}.")
    directory = os.path.dirname(dest_path)
    os.makedirs(directory, exist_ok=True)
    with open(from_path) as f:
        source_markdown = f.read()
    with open(template_path) as f:
        template = f.read()
    content = markdown_to_html_node(source_markdown)
    content = content.to_html()
    title = extract_title(source_markdown)
    new_page = template.replace('{{ Title }}', title)
    new_page = new_page.replace('{{ Content }}', content)
    with open(dest_path, "w") as f:
        f.write(new_page)




