#!env/bin/python
import subprocess
import time
import os
import shutil

from elasticsearch import NotFoundError
from elastipy import connections

DOCS_DIR = "docs-sphinx"
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


def update_tutorial():
    # delete the shapes index if it is present
    try:
        connections.get().indices.delete("elastipy-example-shapes")
        # we need to wait a while it seems, otherwise
        # the notebook does not have any results
        #time.sleep(1)
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
