
from textnode import *
from leafnode import LeafNode
from parentnode import ParentNode
from inline_markdown import *
from markdown_blocks import markdown_to_blocks
from blocktype import block_to_blockType, BlockType
from recursivecopy import copy_tree
from generate import generate_page, generate_pages_recursive
import os
import shutil
import sys
def main():
    #delete everything in public
    base_path = sys.argv[1] if len(sys.argv) > 1 else "/"
    if os.path.exists("docs"):
        shutil.rmtree("docs")
    os.makedirs("docs")

    generate_pages_recursive(base_path, "content", "template.html", "docs")
    #copy static to public
    copy_tree("static", "docs")

if __name__ == "__main__":
    main()