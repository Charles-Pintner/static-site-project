import os
from markdown_blocks import markdown_to_html_node

def extract_title(markdown: str) -> str:
    for line in markdown.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    raise Exception("No h1 header found in markdown")

def generate_page(from_path, template_path, dest_path):
    print(
        f"Generating page from {from_path} "
        f"to {dest_path} using {template_path}"
    )

    # Read markdown
    with open(from_path, "r") as f:
        markdown = f.read()

    # Read template
    with open(template_path, "r") as f:
        template = f.read()

    # Convert markdown → HTML
    html_node = markdown_to_html_node(markdown)
    html_content = html_node.to_html()

    # Extract title
    title = extract_title(markdown)

    # Replace placeholders
    full_html = (
        template
        .replace("{{ Title }}", title)
        .replace("{{ Content }}", html_content)
    )

    # Ensure destination directory exists
    dirname = os.path.dirname(dest_path)
    if dirname:
        os.makedirs(dirname, exist_ok=True)

    # Write output file
    with open(dest_path, "w") as f:
        f.write(full_html)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    # Ensure the destination directory exists
    os.makedirs(dest_dir_path, exist_ok=True)

    for entry in os.listdir(dir_path_content):
        content_entry_path = os.path.join(dir_path_content, entry)
        dest_entry_path = os.path.join(dest_dir_path, entry)

        # If it's a directory, recurse
        if os.path.isdir(content_entry_path):
            generate_pages_recursive(
                content_entry_path,
                template_path,
                dest_entry_path
            )

        # If it's a markdown file, generate an HTML page
        elif entry.endswith(".md"):
            dest_html_path = dest_entry_path.replace(".md", ".html")
            generate_page(
                content_entry_path,
                template_path,
                dest_html_path
            )
