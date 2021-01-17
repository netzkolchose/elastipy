#!env/bin/python
"""
Run this file to create rst versions from doc-related notebooks.

All notebooks are executed and require a running elasticsearch at localhost:9200
"""
import subprocess
import time
import os
import shutil

from elasticsearch import NotFoundError
from elastipy import connections

DOCS_DIR = "docs"
HIDDEN_CELLS = [
    r"^# hidden.*",
]


def export_notebook(filename):
    env = os.environ.copy()
    env["PYTHONPATH"] = ".."
    result = subprocess.call(
        [
            "jupyter", "nbconvert",
            "--execute", "--to=rst", f"--output-dir={DOCS_DIR}",
            f"--RegexRemovePreprocessor.patterns={repr(HIDDEN_CELLS)}",
            filename,
        ],
        env=env,
    )
    if result:
        raise AssertionError(
            f"Exporting notebook {filename} failed with exit-code {result}"
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

    export_notebook("examples/tutorial.ipynb")
    rename_lexer("docs/tutorial.rst", "ipython3", "python3")


if __name__ == "__main__":
    render_tutorial()
