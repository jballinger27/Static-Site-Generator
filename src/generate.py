from markdown_blocks import extract_title, markdown_to_html_node


def generate_page(basepath, from_path, template_path, to_path):
    markdown = ""
    with open(from_path, 'r') as f:
        markdown = f.read()
    title = extract_title(markdown)
    content_node = markdown_to_html_node(markdown)
    with open(template_path, 'r') as f:
        template = f.read()
    html = template.replace("{{ Title }}", title).replace("{{ Content }}", content_node.to_html())

    final = html.replace('href="/', f'href="{basepath}').replace('src="/', f'src="{basepath}')
    with open(to_path, 'w') as f:
        f.write(final)

def generate_pages_recursive(basepath, content_dir, template, output_dir):
    import os
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    for item in os.listdir(content_dir):
        item_path = os.path.join(content_dir, item)
        if os.path.isdir(item_path):
            new_output_dir = os.path.join(output_dir, item)
            generate_pages_recursive(basepath, item_path, template, new_output_dir)
        elif item.endswith(".md"):
            from_path = item_path
            to_filename = item[:-3] + ".html"
            to_path = os.path.join(output_dir, to_filename)
            generate_page(basepath, from_path, template, to_path)