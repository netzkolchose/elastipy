import argparse
import re
import subprocess
import os
from dateutil.parser import parser as date_parser

from helper import Exporter


def parse_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "index", type=str,
        help="Postfix for the elasticsearch index where the commits are stored"
    )

    parser.add_argument(
        "repo", type=str,
        help="Name of a directory that contains a github repository"
    )

    return parser.parse_args()


class CommitExporter(Exporter):
    INDEX_NAME = "elastipy-example-commits"

    MAPPINGS = {
        "properties": {
            "timestamp": {"type": "date"},
            "timestamp_hour": {"type": "integer"},
            "timestamp_weekday": {"type": "keyword"},

            "project": {"type": "keyword"},
            "hash": {"type": "keyword"},
            "author": {"type": "keyword"},
            "author_email": {"type": "keyword"},
            "message": {"type": "text"},

            "file": {"type": "keyword"},
            "filepath": {"type": "keyword"},
            "additions": {"type": "integer"},
            "deletions": {"type": "integer"},
        }
    }

    def get_document_id(self, es_data) -> str:
        return es_data["hash"]

    def transform_document(self, data: dict) -> dict:
        data = data.copy()
        data["timestamp_hour"] = data["timestamp"].hour
        data["timestamp_weekday"] = data["timestamp"].strftime("%w %A")
        return data


def iter_git_commits(path: str):
    """
    Yields a dictionary for every git log that is found
    in the given directoy.

    The ``git log`` command is used to get all the logs.

    :param path: str
    :return: generator of dict
    """
    changes_re = re.compile(r"^(\d+)\s(\d+)\s(.*)$")
    delimiter1 = "$$$1-elastipy-data-delimiter-$$$"
    delimiter2 = "$$$2-elastipy-data-delimiter-$$$"
    git_cmd = f"git log --branches --numstat --pretty='{delimiter1}%n%H%n%an%n%ae%n%cI%n%B{delimiter2}'"

    output = subprocess.check_output(
        ["bash", "-c", f"cd {path} && {git_cmd}"]
    ).decode("utf-8")

    for entry in output.split(delimiter1):
        if entry:
            entry1, entry2 = entry.split(delimiter2)

            entry1 = entry1.strip().splitlines()

            commit = {
                "hash": entry1[0],
                "author": entry1[1],
                "author_email": entry1[2],
                "timestamp": date_parser().parse(entry1[3]),
                "message": "\n".join(entry1[4:]),
                "changes": [],
            }
            for line in entry2.splitlines():
                change_match = changes_re.match(line)
                if change_match:
                    groups = change_match.groups()
                    commit.update({
                        "filepath": groups[2],
                        "file": groups[2].split(os.path.sep)[-1],
                        "additions": int(groups[0]),
                        "deletions": int(groups[1]),
                    })

            yield commit


if __name__ == "__main__":
    args = parse_arguments()

    exporter = CommitExporter(index_postfix=args.index)

    exporter.export_list(
        iter_git_commits(args.repo),
        verbose=True,
    )
