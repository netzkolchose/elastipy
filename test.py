#!env/bin/python
import os
import subprocess
import argparse
import json
import time
from typing import Sequence, Mapping

import elasticsearch

from elastipy import connections


def parse_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--live", type=bool, default=False, nargs="?", const=True,
        help="Test against elasticsearch backend"
    )
    parser.add_argument(
        "--failfast", type=bool, default=False, nargs="?", const=True,
        help="Stop at first error"
    )
    parser.add_argument(
        "-es", "--elasticsearch", type=str, default=None,
        help="Json representation of elasticsearch server settings"
    )
    parser.add_argument(
        "-m", "--missing", type=bool, default=False, nargs="?", const=True,
        help="Show missing line numbers in coverage report"
    )

    return parser.parse_args()


def check_cluster_ready(params: str = None, max_seconds: int = 60, interval: int = 5):
    """
    Wait that elasticsearch cluster is connected and ready
    """
    # override default connection
    if params:
        connections.set("default", json.loads(params))

    for i in range(0, max_seconds, interval):
        try:
            health = connections.get("default").cat.health(format="json")

            health = health[0]  # expect at least one node

            if health["status"] != "red":
                return
            print("waiting for elasticsearch status change:", health["status"])

        except elasticsearch.ConnectionError:
            print("waiting for elasticsearch server")

        time.sleep(interval)

    print("elasticsearch server not available")
    exit(1)


def run_test(package_names: Sequence[str], extra_args, extra_env: Mapping = None):
    env = os.environ.copy()
    if extra_env:
        env.update(extra_env)

    return subprocess.call(
        ["coverage", "run", "-m", "unittest", *extra_args, *package_names],
        env=env
    )


if __name__ == "__main__":

    options = parse_arguments()

    extra_args = []
    extra_env = dict()
    package_names = ["tests"]

    if options.live:
        package_names.append("tests.live")
        check_cluster_ready(options.elasticsearch)

    if options.failfast:
        extra_args.append("--failfast")

    if options.elasticsearch:
        extra_env["ELASTIPY_UNITTEST_SERVER"] = options.elasticsearch

    code = run_test(package_names, extra_args=extra_args, extra_env=extra_env)
    if code:
        exit(code)

    report_args = []

    if options.missing:
        report_args.append("--show-missing")

    subprocess.call(["coverage", "report", *report_args])
