import math
from typing import Tuple, Union


def geotile_to_lat_lon(
        tile: Union[str, Tuple[int, int, int]],
        offset: Tuple[float, float] = (.5, .5),
) -> Tuple[float, float]:
    """
    Convert an elasticsearch geotile key to a latitude/longitude tuple

    Specific implementation is adapted from bing-map's
    `quadtile example code <https://docs.microsoft.com/en-us/bingmaps/articles/bing-maps-tile-system`__.

    :param tile:
        - a **string** in the form ``<zoom>/<x>/<y>``
        - or a **tuple** containing ``zoom``, ``x`` and ``y`` as integers

    :param offset:
        A float tuple that defines the offset inside the map-tile
        in range ``[0, 1]``. Defaults to the center of the tile: ``(.5, .5)``

    :return: tuple of latitude and longitude as float
    """
    if isinstance(tile, tuple):
        zoom, x, y = tile
    else:
        zoom, x, y = (int(i) for i in tile.split("/"))

    num_tiles = 2 ** zoom
    x = (x + offset[0]) / num_tiles
    y = (y + offset[1]) / num_tiles

    lon = 360. * x - 180.
    lat = 90. - 360. * math.atan(math.exp((y - .5) * 2 * math.pi)) / math.pi

    return lat, lon


def geohash_to_lat_lon(
        hash: str,
) -> Tuple[float, float]:
    """
    Convert a `geohash <https://en.wikipedia.org/wiki/Geohash>`__ to
    a tuple with latitude and longitude.

    Uses `pygeohash <https://github.com/wdm0006/pygeohash>`__.decode()
    so the package must be installed.

    :param hash: The geohash string

    :return: tuple of latitude and longitude as float
    """
    import pygeohash
    return pygeohash.decode(hash)
