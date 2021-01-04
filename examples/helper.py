import os
import sys

import requests

# make sure we find the package, even if it's not installed
try:
    from elastipy import Exporter, Search, query
except ImportError:
    sys.path.insert(0, "..")
    from elastipy import Exporter, Search, query


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
    :param filename: filename without path
    :return: str, filename with path
    """
    cache_filename = os.path.join(
        CACHE_DIR,
        filename,
    )
    if os.path.exists(cache_filename):
        return cache_filename

    response = requests.get(url)

    if not os.path.exists(CACHE_DIR):
        os.makedirs(CACHE_DIR)

    with open(cache_filename, "wb") as fp:
        fp.write(response.content)

    return cache_filename

