import argparse
import requests

from helper import Exporter


def parse_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "repo", type=str,
        help="Full name of a public github repository like 'owner/repo-name'"
    )

    return parser.parse_args()


def iter_commits(full_name: str):
    session = requests.session()
    session.headers.update({
        "Accept": "application/vnd.github.v3+json"
    })

    per_page = 100
    page = 0

    while True:
        response = session.get(
            f"https://api.github.com/repos/{full_name}/commits",
            params={"per_page": per_page, "page": page}
        )
        commits = response.json()
        for commit in commits:
            yield commit

        if len(commits) < per_page:
            break
        page += 1


ACCEPTED_INDEX_CHARS = set("abcdefghijklmnopqrstuvwxyz0123456789-")


class CommitExporter(Exporter):
    INDEX_NAME = "elastipy-example-commits-*"
    MAPPINGS = {
        "properties": {
            "project": {"type": "keyword"},
            "sha": {"type": "keyword"},
            "date": {"type": "date"},
            "author": {"type": "keyword"},
            "github_author": {"type": "keyword"},
            "message": {"type": "text"},
        }
    }

    def get_document_index(self, es_data) -> str:
        prefix = "".join(
            c if c in ACCEPTED_INDEX_CHARS else "-"
            for c in es_data["project"].lower()
        )
        return self.index_name().replace("*", prefix)

    def get_document_id(self, es_data) -> str:
        return es_data["sha"]

    def transform_document(self, data):
        #import json
        #print(json.dumps(data, indent=2))

        return {
            "project": self.github_project,
            "sha": data["sha"],
            "date": data["commit"]["author"]["date"],
            "author": data["commit"]["author"]["name"],
            "github_author": data["author"]["login"],
            "message": data["commit"]["message"],
        }


if __name__ == "__main__":
    args = parse_arguments()

    exporter = CommitExporter()
    exporter.github_project = args.repo

    exporter.export_list(
        iter_commits(args.repo),
        verbose=True,
    )
