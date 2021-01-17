#!env/bin/python
import subprocess
import time
import glob
import pathlib
import shutil

from elasticsearch import NotFoundError
from elastipy import connections

DOCS_DIR = "docs-sphinx"
HIDDEN_RE = "^# hidden.*"


def export_notebook(filename):
    result = subprocess.call([
        "jupyter", "nbconvert", "--to=rst", f"--output-dir={DOCS_DIR}",
        f"--RegexRemovePreprocessor.patterns=['{HIDDEN_RE}']",
        filename,
    ])
    if result:
        raise AssertionError(
            f"Exporting notebook {filename} failed with exit-code {result}"
        )


def update_tutorial():
    # delete the shapes index if it is present
    try:
        connections.get().indices.delete("elastipy-example-shapes")
        # we need to wait a while it seems, otherwise
        # the notebook does not have any results
        time.sleep(1)
    except NotFoundError:
        pass

    # remove the previous files
    try:
        shutil.rmtree(f"{DOCS_DIR}/tutorial_files")
    except FileNotFoundError:
        pass

    export_notebook("examples/tutorial.ipynb")


if __name__ == "__main__":
    update_tutorial()
