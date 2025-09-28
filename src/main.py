
from textnode import *
from leafnode import LeafNode
from parentnode import ParentNode
from inline_markdown import *
from markdown_blocks import markdown_to_blocks
from blocktype import block_to_blockType, BlockType
from recursivecopy import copy_tree
from generate import generate_page, generate_pages_recursive

def main():
    #delete everything in public
    import os
    import shutil
    if os.path.exists("public"):
        shutil.rmtree("public")
    os.makedirs("public")

    generate_pages_recursive("content", "templates", "public")
    #copy static to public
    copy_tree("static", "public")

if __name__ == "__main__":
    main()