import argparse
import requests
import getpass
import time

from helper import Exporter


def parse_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "repo", type=str,
        help="Full name of a public github repository like 'owner/repo-name'"
    )

    parser.add_argument(
        "-o", "--offset", type=int, nargs="?", default=0,
        help="offset into commit list (is divided by page_count==100)",
    )

    parser.add_argument(
        "-u", "--user", type=str, nargs="?", default=None,
        help="github username for http basic auth",
    )

    return parser.parse_args()


def iter_commits(full_name: str, offset: int = 0, user: str = None):
    requests_per_hour = 60

    session = requests.Session()
    session.headers.update({
        "Accept": "application/vnd.github.v3+json"
    })

    if user:
        pw = getpass.getpass("github password")
        session.auth = (user, pw)

    per_page = 100
    page = offset // per_page

    throttling_time = 60 * 60 / requests_per_hour

    while True:
        request_time = time.time()

        response = session.get(
            f"https://api.github.com/repos/{full_name}/commits",
            params={"per_page": per_page, "page": page}
        )
        requests_per_hour = response.headers["X-RateLimit-Limit"]

        if response.status_code != 200:
            print(f"response status {response.status_code}")
            print(response.json())
            exit(1)

        commits = response.json()
        for commit in commits:
            yield commit

        if len(commits) < per_page:
            break

        page += 1
        request_time = time.time() - request_time

        if request_time < throttling_time:
            time.sleep(throttling_time - request_time)


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
            "comment_count": {"type": "integer"},
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
        import json
        print(json.dumps(data, indent=2))

        return {
            "project": self.github_project,
            "sha": data["sha"],
            "date": data["commit"]["author"]["date"],
            "author": data["commit"]["author"]["name"],
            "github_author": (data.get("author") or {}).get("login") or (data.get("committer") or {}).get("login"),
            "message": data["commit"]["message"],
            "comment_count": data["commit"]["comment_count"],
        }


if __name__ == "__main__":
    args = parse_arguments()

    exporter = CommitExporter()
    exporter.github_project = args.repo

    exporter.export_list(
        iter_commits(args.repo, user=args.user),
        verbose=True,
    )
