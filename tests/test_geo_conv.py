import unittest
from typing import Sequence

from elastipy import geo_conv


class TestGeoConv(unittest.TestCase):

    def assertCoordsEqual(self, expected: Sequence, real: Sequence, decimals: int = 4):
        expected = tuple(round(i, decimals) for i in expected)
        real = tuple(round(i, decimals) for i in real)
        self.assertEqual(expected, real, f"Expected {expected}, got {real}")

    def test_geotile_lon_lat(self):
        self.assertCoordsEqual((0, 0), geo_conv.geotile_to_lon_lat("0/0/0"))
        self.assertCoordsEqual((0, 0), geo_conv.geotile_to_lon_lat((0, 0, 0)))
        self.assertCoordsEqual((180, 0), geo_conv.geotile_to_lon_lat("0/0/0", offset=(1, .5)))
        self.assertCoordsEqual((-180, 0), geo_conv.geotile_to_lon_lat("0/0/0", offset=(0, .5)))
        self.assertCoordsEqual((0, 85.051129), geo_conv.geotile_to_lon_lat("0/0/0", offset=(.5, 0)))
        self.assertCoordsEqual((0, -85.051129), geo_conv.geotile_to_lon_lat("0/0/0", offset=(.5, 1)))

    def test_geotile_lat_lon(self):
        self.assertCoordsEqual((0, 0), geo_conv.geotile_to_lat_lon("0/0/0"))
        self.assertCoordsEqual((0, 0), geo_conv.geotile_to_lat_lon((0, 0, 0)))
        self.assertCoordsEqual((0, 180), geo_conv.geotile_to_lat_lon("0/0/0", offset=(.5, 1)))
        self.assertCoordsEqual((0, -180), geo_conv.geotile_to_lat_lon("0/0/0", offset=(.5, 0)))
        self.assertCoordsEqual((85.051129, 0), geo_conv.geotile_to_lat_lon("0/0/0", offset=(0, .5)))
        self.assertCoordsEqual((-85.051129, 0), geo_conv.geotile_to_lat_lon("0/0/0", offset=(1, .5)))

    def test_geohash_lon_lat(self):
        self.assertCoordsEqual((-157.5, -67.5), geo_conv.geohash_to_lon_lat("0"))
        self.assertCoordsEqual((-112.5, -67.5), geo_conv.geohash_to_lon_lat("1"))
        self.assertCoordsEqual((89.0112, 25.3784), geo_conv.geohash_to_lon_lat("tux23"))
        
    def test_geohash_lat_lon(self):
        self.assertCoordsEqual((-67.5, -157.5), geo_conv.geohash_to_lat_lon("0"))
        self.assertCoordsEqual((-67.5, -112.5), geo_conv.geohash_to_lat_lon("1"))
        self.assertCoordsEqual((25.3784, 89.0112), geo_conv.geohash_to_lat_lon("tux23"))



if __name__ == "__main__":
    unittest.main()
