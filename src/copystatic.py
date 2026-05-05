import os
import shutil
from pathlib import Path
from markdown_blocks import block_to_block_type, markdown_to_blocks, markdown_to_html_node
from htmlnode import HTMLNode

def generator(source_dir, dest_dir):
    if not os.path.exists(dest_dir):
        os.mkdir(dest_dir)
    source_list = os.listdir(source_dir)
    for name in source_list:
        source_file_path = os.path.join(source_dir, name)
        dest_file_path = os.path.join(dest_dir, name)
        if os.path.isfile(source_file_path):
            shutil.copy(source_file_path, dest_file_path)
        if os.path.isdir(source_file_path):
            os.mkdir(dest_file_path)
            generator(source_file_path, dest_file_path)

def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            title = line[2:]
            title = title.rstrip()
            return title
    raise Exception("no heading found")

def generate_page(from_path, template_path, dest_path, basepath):
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
    new_page = new_page.replace('href="/', f'href="{basepath}')
    new_page = new_page.replace('src="/', f'src="{basepath}')
    with open(dest_path, "w") as f:
        f.write(new_page)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    source_content = os.listdir(dir_path_content)
    for each in source_content:
        source = os.path.join(dir_path_content, each)
        if os.path.isfile(source):
            destination_path = os.path.join(dest_dir_path, each)
            destination_path = Path(destination_path).with_suffix(".html")
            generate_page(source, template_path, destination_path, basepath)
        else:
            recursed_destination = os.path.join(dest_dir_path, each)
            generate_pages_recursive(source, template_path, recursed_destination, basepath)


