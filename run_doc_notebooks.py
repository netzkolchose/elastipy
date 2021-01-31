#!env/bin/python
"""
Run this file to create rst versions from doc-related notebooks.

All notebooks are executed and require a running elasticsearch at localhost:9200
"""
import subprocess
import time
import os
import shutil
import shutil

from elasticsearch import NotFoundError
from elastipy import connections

DOCS_DIR = "docs"
HIDDEN_CELLS = [
    r"^# hidden.*",
]
RUN_BUT_HIDDEN_CELLS = [
    "# run-but-hidden"
]


def export_notebook(filename, format, directory, do_rename_lexer=True):
    env = os.environ.copy()
    env["PYTHONPATH"] = ".."
    result = subprocess.call(
        [
            "jupyter", "nbconvert",
            "--execute", f"--to={format}", f"--output-dir={directory}",
            f"--RegexRemovePreprocessor.patterns={repr(HIDDEN_CELLS)}",
            filename,
        ],
        env=env,
    )
    if result:
        raise AssertionError(
            f"Exporting notebook {filename} failed with exit-code {result}"
        )

    ext = {"markdown": "md"}.get(format, format)
    out_filename = filename.split(os.path.sep)[-1].replace(".ipynb", f".{ext}")

    if do_rename_lexer:
        # rename the "ipython3" lexer so readthedocs does not need ipython installed
        #   It's safe because we do not use cell magic or other extended stuff
        rename_lexer(
            os.path.join(directory, out_filename),
            "ipython3",
            "python3"
        )

    if format == "markdown":
        remove_hidden_cells_in_markdown(out_filename)


def rename_lexer(filename, old, new):
    with open(filename, "r") as fp:
        text = fp.read()
    replaced_text = text.replace(
        f".. code:: {old}",
        f".. code:: {new}",
    )
    if replaced_text != text:
        print(f"renaming lexer {old} to {new} in {filename}")
        with open(filename, "w") as fp:
            fp.write(replaced_text)


def remove_hidden_cells_in_markdown(filename: str):
    """
    Loads a markdown file and removes all ``` blocks that
    have the line "# run-but-hidden" in them.

    Unfortunately the jupyter nbconvert RegexRemovePreprocessor removes
    all hidden cells before execution, so if we need to run them but hide
    the output this crappy patching is required.
    """
    with open(filename) as fp:
        lines = fp.read().splitlines()

    out_lines = []
    block_lines = []
    inside_block = False
    block_hidden = False
    for line in lines:
        if line.startswith("```"):
            if not inside_block:
                inside_block = True
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

            for tag in RUN_BUT_HIDDEN_CELLS:
                if line.startswith(tag):
                    block_hidden = True
                    break

        else:
            out_lines.append(line)

    if lines != out_lines:
        print(f"removing hidden cells from {filename}")
        text = "\n".join(out_lines)
        with open(filename, "w") as fp:
            fp.write(text)


def render_tutorial():
    # delete the shapes index if it is present
    try:
        connections.get().indices.delete("elastipy-example-shapes")
    except NotFoundError:
        pass

    # remove the previous files
    try:
        shutil.rmtree(f"{DOCS_DIR}/tutorial_files")
    except FileNotFoundError:
        pass

    export_notebook("examples/tutorial.ipynb", "rst", DOCS_DIR)


def render_quickref():
    """
    Renders the docs/quickref.ipynb notebook, converts to markdown
    and inserts the stuff into the README.md
    """
    export_notebook("docs/quickref.ipynb", "markdown", ".")

    with open("quickref.md") as fp:
        quickref = fp.read().strip()

    README_START = "### configuration"
    README_END = "**More examples can be found [here](examples).**"

    with open("README.md") as fp:
        readme = fp.read()

    index_start = readme.index(README_START)
    index_end = readme.index(README_END)

    old_readme = readme
    readme = readme[:index_start] + quickref + readme[index_end:]

    if readme != old_readme:
        print(f"Putting quickref into README.md")
        with open("README.md", "w") as fp:
            fp.write(readme)

    os.remove("quickref.md")


if __name__ == "__main__":
    render_tutorial()
    render_quickref()
