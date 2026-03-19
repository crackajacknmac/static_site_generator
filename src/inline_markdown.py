import re
from textnode import TextType, TextNode

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            node_parts = node.text.split(delimiter)
            if len(node_parts) == 1:
                new_nodes.append(node)
            elif len(node_parts) % 2 == 0:
                raise Exception('Invalid Markdown')
            else:
                fresh_node = []
                for i in range(len(node_parts)):
                    part = node_parts[i]
                    if part == "":
                        continue
                    if i % 2 == 0:
                        fresh_node.append(TextNode(part, TextType.TEXT))
                    else:
                        fresh_node.append(TextNode(part, text_type))
                new_nodes.extend(fresh_node)
    return new_nodes


def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        image = extract_markdown_images(node.text)
        if len(image) == 0:
            new_nodes.append(node)
            continue
        remaining = node.text
        for img_alt, img_url in image:
            sections = remaining.split(f"![{img_alt}]({img_url})", 1)
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(img_alt, TextType.IMAGE, img_url))
            remaining = sections[1]
        if remaining != "":
            new_nodes.append(TextNode(remaining, TextType.TEXT))
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        link = extract_markdown_links(node.text)
        if len(link) == 0:
            new_nodes.append(node)
            continue
        remaining = node.text
        for link_alt, link_url in link:
            sections = remaining.split(f"[{link_alt}]({link_url})", 1)
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(link_alt, TextType.LINK, link_url))
            remaining = sections[1]
        if remaining != "":
            new_nodes.append(TextNode(remaining, TextType.TEXT))
    return new_nodes
