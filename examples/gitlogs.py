import argparse
import re
import subprocess
import os
from dateutil.parser import parser as date_parser

from tqdm import tqdm

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

    parser.add_argument(
        "-d", "--delete", type=bool, nargs="?", default=False, const=True,
        help="Delete the elasticsearch index before sending documents"
    )

    parser.add_argument(
        "-o", "--offset", type=int, nargs="?", default=0,
        help="Start exporting at a specific position"
             " (logs still need to be piped up to this point)"
    )

    parser.add_argument(
        "-q", "--quiet", type=bool, nargs="?", default=False, const=True,
        help="Do not display progress using <tqdm> (defaults to False)"
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
            "message": {
                "type": "text",
                "analyzer": "stop",
                "term_vector": "with_positions_offsets_payloads",
                "store": True,
                "fielddata": True,
            },

            "changes.file": {"type": "keyword"},
            "changes.filepath": {"type": "keyword"},
            "changes.additions": {"type": "integer"},
            "changes.deletions": {"type": "integer"},
        }
    }

    def get_document_id(self, es_data) -> str:
        return es_data["hash"]

    def transform_document(self, data: dict) -> dict:
        data = data.copy()
        data["timestamp_hour"] = data["timestamp"].hour
        data["timestamp_weekday"] = data["timestamp"].strftime("%w %A")
        data["project"] = self.index_postfix
        return data


def iter_git_commits(path: str, skip: int = 0):
    """
    Yields a dictionary for every git log that is found
    in the given directoy.

    The ``git log`` command is used to get all the logs.

    :param path: str
        Directory of git repository

    :param skip: int
        Skip these number of commits before yielding.
        (via git log --skip parameter)

    :return: generator of dict
    """
    changes_re = re.compile(r"^(\d+)\s(\d+)\s(.*)$")
    delimiter1 = "$$$1-elastipy-data-delimiter-$$$"
    delimiter2 = "\n$$$2-elastipy-data-delimiter-$$$"
    git_cmd = f"git log --all --numstat --pretty='{delimiter1}%n%H%n%an%n%ae%n%cI%n%B{delimiter2}'"
    if skip:
        git_cmd += f" --skip {skip}"

    process = subprocess.Popen(
        ["bash", "-c", f"cd {path} && {git_cmd}"],
        stdout=subprocess.PIPE,
    )

    commit = dict()
    current_line = 0
    while True:
        line = process.stdout.readline()
        if not line:
            break

        line = line

        line = safe_decode(line).rstrip()

        # a new commit starts
        if line == delimiter1:
            if commit:
                yield commit
            commit = dict()
            current_line = 0

        # commit message ended and changes (numstats) follow
        elif line == delimiter2[1:]:
            current_line = -1

        # digest each line
        else:
            if current_line == 1:
                commit["hash"] = line
            elif current_line == 2:
                commit["author"] = line
            elif current_line == 3:
                commit["author_email"] = line
            elif current_line == 4:
                commit["timestamp"] = date_parser().parse(line)
            elif current_line == 5:
                commit["message"] = line
            elif current_line > 5:
                commit["message"] += "\n" + line

            elif current_line == -1:
                change_match = changes_re.match(line)
                if change_match:
                    if "changes" not in commit:
                        commit["changes"] = []

                    groups = change_match.groups()
                    commit["changes"].append({
                        "filepath": groups[2],
                        "file": groups[2].split(os.path.sep)[-1],
                        "additions": int(groups[0]),
                        "deletions": int(groups[1]),
                    })

        if current_line >= 0:
            current_line += 1

    if commit:
        yield commit

    process.kill()
    process.wait()


def iter_git_commits_verbose(path: str, offset: int = 0, verbose: bool = True):
    """
    Yields a dictionary for every git log that is found
    in the given directoy.

    The ``git log`` command is used to get all the logs.

    :param path: str
        Directory of git repository

    :param offset: int
        Offset after which to yield commits

    :param verbose: bool
        If True, uses ``tqdm`` to display progress

    :return: generator of dict
    """
    generator = iter_git_commits(path, skip=offset)

    if verbose:
        num_commits = subprocess.check_output(
            ["bash", "-c", f"cd {path} && git rev-list --all --count"],
        )
        num_commits = int(num_commits)

        generator = tqdm(generator, total=num_commits - offset)

    for commit in generator:
        yield commit


def safe_decode(s: bytes):
    for encoding in ("utf-8", "latin1"):
        try:
            return s.decode(encoding)
        except UnicodeDecodeError:
            pass
    return s.decode("utf-8", errors="ignore")


if __name__ == "__main__":
    args = parse_arguments()

    exporter = CommitExporter(index_postfix=args.index)

    if args.delete:
        exporter.delete_index()

    exporter.export_list(
        iter_git_commits_verbose(
            path=args.repo,
            offset=args.offset,
            verbose=not args.quiet,
        )
    )
