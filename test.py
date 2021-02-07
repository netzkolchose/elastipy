#!env/bin/python
import os
import subprocess
import argparse
import json
import time
import fnmatch
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
        "-c", "--coverage", type=bool, default=False, nargs="?", const=True,
        help="Show coverage report"
    )
    parser.add_argument(
        "-m", "--missing", type=bool, default=False, nargs="?", const=True,
        help="Show missing line numbers in coverage report"
    )
    parser.add_argument(
        "-i", "--include", type=str, nargs="+",
        help="wildcard patterns to match specific tests"
    )
    parser.add_argument(
        "-e", "--exclude", type=str, nargs="+",
        help="wildcard patterns to exclude specific tests"
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


def run_test(
        package_names: Sequence[str],
        extra_args,
        extra_env: Mapping = None,
        coverage: bool = False,
):
    env = os.environ.copy()
    if extra_env:
        env.update(extra_env)

    if coverage:
        return subprocess.call(
            ["coverage", "run", "-m", "unittest", *extra_args, *package_names],
            env=env
        )
    else:
        return subprocess.call(
            ["python", "-m", "unittest", *extra_args, *package_names],
            env=env
        )


def get_test_names(package_names: list, include: list, exclude: list) -> list:
    """
    Return a list of strings passable as arguments to `python -m unittest`
    which contain all tests that match any one of the wildcard patterns
    :param package_names: `list[str]`
    :param include: `list[str]` or None
    :param exclude: `list[str]` or None
    :return: `list[str]`
    """
    import unittest
    import inspect
    import importlib

    if include is not None:
        include = [
            f"*{p}*" if "*" not in p and "?" not in p else p
            for p in include
        ]

    if exclude is not None:
        exclude = [
            f"*{p}*" if "*" not in p and "?" not in p else p
            for p in exclude
        ]

    classes = set()
    for package_name in package_names:
        module = importlib.import_module(package_name)
        for key in dir(module):
            thing = getattr(module, key)
            if inspect.isclass(thing) and issubclass(thing, unittest.TestCase):
                classes.add(thing)

    names = []
    for klass in classes:
        for key in dir(klass):
            thing = getattr(klass, key)
            if key.startswith("test_") and callable(thing):
                name = f"{klass.__name__}.{thing.__name__}"

                filename = inspect.getfile(inspect.getmodule(klass))[:-3]
                path = filename.split("/")
                path = path[path.index("tests"):]
                path = ".".join(path)

                name = f"{path}.{name}"

                if include is not None:
                    has_match = False
                    for p in include:
                        if fnmatch.fnmatchcase(name, p):
                            has_match = True
                            break
                    if not has_match:
                        continue

                if exclude is not None:
                    has_match = False
                    for p in exclude:
                        if fnmatch.fnmatchcase(name, p):
                            has_match = True
                            break
                    if has_match:
                        continue

                names.append(name)

    return sorted(names)


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

    if options.include or options.exclude:
        extra_args += get_test_names(
            package_names, options.include, options.exclude
        )
        package_names = []
        if not extra_args:
            print("No matches found")
            exit(1)

    code = run_test(package_names, extra_args=extra_args, extra_env=extra_env)
    if code:
        exit(code)

    if options.coverage or options.missing:

        report_args = []

        if options.missing:
            report_args.append("--show-missing")

        subprocess.call(["coverage", "report", *report_args])
