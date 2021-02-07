import os
import sys

import requests

# make sure we find the package, even if it's not installed
try:
    from elastipy import Exporter, Search, query, connections
except ImportError:
    sys.path.insert(0, "..")
    from elastipy import Exporter, Search, query, connections


CACHE_DIR = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "cache"
    )
)


def get_web_file(url: str, filename: str):
    """
    Download from url, return absolute filename

    :param url: str, the place in the wab
    :param filename: filename with optional additional path
    :return: str, filename with path
    """
    full_path = CACHE_DIR
    filename_path = os.path.dirname(filename)
    if filename_path:
        full_path = os.path.join(CACHE_DIR, filename_path)

    if not os.path.exists(full_path):
        os.makedirs(full_path)

    cache_filename = os.path.join(
        CACHE_DIR,
        filename,
    )
    if os.path.exists(cache_filename):
        return cache_filename

    print(f"downloading {url} to {cache_filename}", file=sys.stderr)
    response = requests.get(url)

    if not os.path.exists(CACHE_DIR):
        os.makedirs(CACHE_DIR)

    with open(cache_filename, "wb") as fp:
        fp.write(response.content)

    return cache_filename

