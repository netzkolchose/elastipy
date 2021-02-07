from typing import List
import re


RST_BLOCK_RE = re.compile(r"^\.\. [a-zA-Z\-]+::")


def remove_hidden_cells_in_file(filename: str, patterns: List[str]):
    """
    Loads a markdown file and removes all ``` blocks that
    have the line "# run-but-hidden" in them.

    :param filename: str
    :param patterns: list[str]
        regex patterns that define the 'hidden' clauses

    :return: None
    """
    with open(filename) as fp:
        text = fp.read()

    if filename.lower().endswith(".md"):
        out_text = remove_hidden_cells_markdown(text, patterns)
    elif filename.lower().endswith(".rst"):
        out_text = remove_hidden_cells_rst(text, patterns)
    else:
        raise ValueError(
            "Can not handle file extension '%s'" % filename.split(".")[-1]
        )

    if text != out_text:
        print(f"removing hidden cells from {filename}")
        with open(filename, "w") as fp:
            fp.write(out_text)


def remove_hidden_cells_markdown(text: str, patterns: List[str]):
    """
    Unfortunately the jupyter nbconvert RegexRemovePreprocessor removes
    all hidden cells before execution, so if we need to run them but hide
    the output this crappy patching is required.

    :param text: str, The rst or markdown text
    :param patterns: list[str]
        regex patterns that define the 'hidden' clauses

    :returns: str, The stripped version
    """
    out_lines = []
    block_lines = []
    inside_block = False
    block_hidden = False
    for line in text.splitlines():
        if line.startswith("```"):
            # start block
            if not inside_block:
                inside_block = True
            # end block
            else:
                if not block_hidden:
                    out_lines += block_lines
                    out_lines.append(line)
                block_lines.clear()
                inside_block = False
                block_hidden = False
                continue

        if inside_block:
            block_lines.append(line)

            for pattern in patterns:
                if re.match(pattern, line):
                    block_hidden = True
                    break
        else:
            out_lines.append(line)

    return "\n".join(out_lines)


def remove_hidden_cells_rst(text: str, patterns: List[str]):
    """
    Unfortunately the jupyter nbconvert RegexRemovePreprocessor removes
    all hidden cells before execution, so if we need to run them but hide
    the output this crappy patching is required.

    :param text: str, The rst or markdown text
    :param patterns: list[str]
        regex patterns that define the 'hidden' clauses

    :returns: str, The stripped version
    """
    out_lines = []
    block_lines = []
    inside_block = False
    block_hidden = False
    for line in text.splitlines():

        # start block
        if RST_BLOCK_RE.match(line):
            # end current block
            if inside_block and not block_hidden:
                out_lines += block_lines

            block_lines.clear()
            inside_block = True
            block_hidden = False

        if inside_block:

            # end block ...
            if block_lines and line.strip():
                # ... if there is no indentation
                if line.lstrip() == line:
                    if not block_hidden:
                        out_lines += block_lines

                    block_lines.clear()
                    inside_block = False
                    block_hidden = False

        if inside_block:
            block_lines.append(line)

            for pattern in patterns:
                if re.match(pattern, line.lstrip()):
                    block_hidden = True
                    break
        else:
            out_lines.append(line)

    if inside_block and not block_hidden:
        out_lines += block_lines

    return "\n".join(out_lines)


def fix_links_in_rst(text: str) -> str:
    """
    Fixes :link:s that get corrupted by from-markdown conversion.

        :link:``some`` becomes :link:`some`

    :param text: str
    :return: str
    """
    def _repl(match):
        g = match.groups()
        return f":{g[0]}:`{g[1]}`"

    text = re.sub(
        r":([^:]+):``([^`]+)``",
        _repl,
        text,
    )

    return text


def fix_links_in_rst_file(filename: str):
    with open(filename) as fp:
        text = fp.read()

    fixed_text = fix_links_in_rst(text)

    if fixed_text != text:
        print(f"fixing rst-links from converted markdown in {filename}")
        with open(filename, "w") as fp:
            fp.write(fixed_text)
