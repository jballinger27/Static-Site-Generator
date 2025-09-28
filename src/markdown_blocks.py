
from blocktype import BlockType, block_to_blockType
from leafnode import LeafNode
from parentnode import ParentNode
from texttohtml import text_node_to_html_node, text_to_textnodes
import re


def markdown_to_blocks(markdown):
    # Split on two or more newlines, preserving code blocks
    import re
    # This regex splits on two or more newlines not inside code blocks
    code_block_pattern = re.compile(r'(```[\s\S]*?```)', re.MULTILINE)
    code_blocks = code_block_pattern.findall(markdown)
    temp = code_block_pattern.sub('[[CODE_BLOCK]]', markdown)
    parts = re.split(r'\n{2,}', temp)
    blocks = []
    code_block_idx = 0
    for part in parts:
        part = part.strip()
        if part == '':
            continue
        if part == '[[CODE_BLOCK]]':
            blocks.append(code_blocks[code_block_idx].strip())
            code_block_idx += 1
        else:
            # Remove lines that are only whitespace
            lines = [l.strip() for l in part.split('\n') if l.strip() != '']
            if lines:
                blocks.append('\n'.join(lines))
    return blocks

def mdHeader_to_html_node(block):
    # Count number of leading #
    import re
    match = re.match(r'^(#+)\s*(.*)', block)
    if not match:
        return mdParagraph_to_html_node(block)
    hashes, text = match.groups()
    level = len(hashes) # Header level is number of #
    if level < 1 or level > 6:
        level = 6
    return ParentNode(f"h{level}", [LeafNode(None, text.strip())])

def mdParagraph_to_html_node(block):
    # Remove leading/trailing spaces and join lines with a space
    lines = [l.strip() for l in block.split('\n') if l.strip() != '']
    joined = ' '.join(lines)
    text_nodes = text_to_textnodes(joined)
    html_nodes = [text_node_to_html_node(tn) for tn in text_nodes]
    return ParentNode("p", html_nodes)

def mdCode_to_html_node(block):
    code_lines = block.split('\n')
    if code_lines[0].strip().startswith('```') and code_lines[-1].strip().endswith('```'):
        code_content_lines = code_lines[1:-1]
    else:
        code_content_lines = code_lines
    code_content = '\n'.join([l.lstrip() for l in code_content_lines])
    if not code_content.endswith('\n'):
        code_content += '\n'
    return ParentNode("pre", [ParentNode("code", [LeafNode(None, code_content)])])

def mdBlockquote_to_html_node(block):
    quote_lines = block.split("\n")
    quote_content = "\n".join([line[1:].strip() for line in quote_lines])
    text_nodes = text_to_textnodes(quote_content)
    html_nodes = [text_node_to_html_node(tn) for tn in text_nodes]
    return ParentNode("blockquote", html_nodes)

def mdList_to_html_node(block):
    list_lines = block.split("\n")
    list_items = []
    for line in list_lines:
        line = line.strip()
        item_content = line[2:].strip()
        text_nodes = text_to_textnodes(item_content)
        html_nodes = [text_node_to_html_node(tn) for tn in text_nodes]
        list_items.append(ParentNode("li", html_nodes))
    return ParentNode("ul", list_items)

def ordered_mdList_to_html_node(block):
    list_lines = block.split("\n")
    list_items = []
    for line in list_lines:
        line = line.strip()
        item_content = line[line.index(".")+1:].strip()
        text_nodes = text_to_textnodes(item_content)
        html_nodes = [text_node_to_html_node(tn) for tn in text_nodes]
        list_items.append(ParentNode("li", html_nodes))
    return ParentNode("ol", list_items)

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    html_nodes = []
    for block in blocks:
        type = block_to_blockType(block)
        if type == BlockType.HEADER:
            html_nodes.append(mdHeader_to_html_node(block))
        elif type == BlockType.PARAGRAPH:
            html_nodes.append(mdParagraph_to_html_node(block))
        elif type == BlockType.CODE:
            html_nodes.append(mdCode_to_html_node(block))
        elif type == BlockType.QUOTE:
            html_nodes.append(mdBlockquote_to_html_node(block))
        elif type == BlockType.UNORDERED_LIST:
            html_nodes.append(mdList_to_html_node(block))
        elif type == BlockType.ORDERED_LIST:
            html_nodes.append(ordered_mdList_to_html_node(block))
    return ParentNode("div", html_nodes)

def extract_title(markdown):
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        type = block_to_blockType(block)
        if type == BlockType.HEADER:
            if block.startswith('# '):
                title_words = block.split()[1:]
                return ' '.join(title_words).strip()
    raise Exception("No header found for title")