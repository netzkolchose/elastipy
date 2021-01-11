#!env/bin/python
import os
import subprocess
import argparse
from typing import Sequence, Mapping


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
        "-es", "--elasticsearch", type=str,
        help="Json representation of elasticsearch server settings"
    )

    return parser.parse_args()


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

    if options.failfast:
        extra_args.append("--failfast")

    if options.elasticsearch:
        extra_env["ELASTIPY_UNITTEST_SERVER"] = options.elasticsearch

    code = run_test(package_names, extra_args=extra_args, extra_env=extra_env)
    if code:
        exit(code)

    subprocess.call(["coverage", "report"])
