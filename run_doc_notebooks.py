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
from docs.helper import remove_hidden_cells_in_file, fix_links_in_rst_file


DOCS_DIR = "docs"
HIDDEN_CELLS = [
    r"^# hidden.*",
    r"^<AxesSubplot.*>$",
]
RUN_BUT_HIDDEN_CELLS = [
    r"# run-but-hidden",
    r"# run-but-hide"
]


def export_notebook(
        filename: str,
        format: str,
        directory: str,
        do_rename_lexer: bool = True
):
    env = os.environ.copy()
    env["PYTHONPATH"] = ".."
    result = subprocess.call(
        [
            "jupyter", "nbconvert",
            "--execute",
            f"--to={format}", f"--output-dir={directory}",
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

    remove_hidden_cells_in_file(
        os.path.join(directory, out_filename),
        HIDDEN_CELLS + RUN_BUT_HIDDEN_CELLS
    )

    if format == "rst":
        fix_links_in_rst_file(
            os.path.join(directory, out_filename)
        )


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
        quickref = fp.read().strip() + "\n\n"

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


def render_gitlogs_example():
    """
    Renders the examples/gitlogs.ipynb notebook
    """
    export_notebook("examples/gitlogs.ipynb", "rst", os.path.join(DOCS_DIR, "examples"))


if __name__ == "__main__":
    render_tutorial()
    render_quickref()
    render_gitlogs_example()
