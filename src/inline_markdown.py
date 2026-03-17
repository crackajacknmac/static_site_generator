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
