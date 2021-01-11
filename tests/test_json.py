import datetime
import unittest
from decimal import Decimal

from elastipy import make_json_compatible


class TestJson(unittest.TestCase):

    def assertJsonConversion(self, data, expected):
        self.assertEqual(
            expected,
            make_json_compatible(data)
        )
        self.assertEqual(
            {"sub": expected},
            make_json_compatible({"sub": data})
        )
        self.assertEqual(
            {"sublist": [expected]},
            make_json_compatible({"sublist": [data]})
        )

    def test_date(self):
        self.assertJsonConversion(
            {
                "dt": datetime.datetime(2000, 1, 1)
            },
            {
                "dt": "2000-01-01T00:00:00"
            },
        )

    def test_to_dict(self):

        class ToDict:
            def __init__(self, kwargs):
                self.kwargs = kwargs

            def to_dict(self):
                return self.kwargs

        self.assertJsonConversion(
            {
                "wrapped": ToDict({
                    "a": 1,
                    "dt": datetime.datetime(2000, 1, 1),
                })
            },
            {
                "wrapped": {
                    "a": 1,
                    "dt": "2000-01-01T00:00:00"
                }
            },
        )

    def test_raise(self):
        class Unknown:
            pass

        with self.assertRaises(TypeError):
            make_json_compatible({"u": Unknown()})


if __name__ == "__main__":
    unittest.main()
