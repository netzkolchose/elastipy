import os


class UnicodeCharacters:
    """
    https://unicode.org/charts/PDF/U2580.pdf

    also interesting: https://en.wikipedia.org/wiki/Box-drawing_character
    """
    quadrants = ("▖", "▘", "", "▝", "▗")
    quadrants3 = ("▙", "▛", "▜", "▟")
    quadrants2 = ("▞", "▚")
    left8th = ("▏", "▎", "▍", "▌", "▋", "▊", "▉")
    bottom8th = ("▁", "▂", "▃", "▄", "▅", "▆", "▇")
    block = "█"
    top = "▀"
    right = "▐"
    shade = ("░", "▒", "▓")
    line_hori = "─"
    line_vert = "│"
    line_cross = "┼"

    @classmethod
    def hbar(cls, v, width):
        """
        Return a string containing a horizontal bar
        :param v: float, in range [0, 1]
        :param width: int, number of characters
        :return: str
        """
        return cls._bar(v, width, cls.left8th)

    @classmethod
    def _bar(cls, v, width, characters):
        v = v * width
        v_floor = int(v)
        v_fract = v - int(v)
        num_char = len(characters)
        ret = cls.block * v_floor
        if v_fract >= 1. / (num_char + 1):
            rest = int(v_fract * num_char)
            ret += characters[rest]
        return ret


class UnicodePixels:

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.pixels = [
            [0.] * self.width
            for h in self.height
        ]

    def pixel_add(self, x, y, amount=1.):
        x, y = int(x + .5), int(y + .5)
        if 0 <= x < self.width and 0 <= y <= self.height:
            self.pixels[y][x] += amount

    def value_range(self):
        v_min, v_max = self.pixels[0][0]
        for y in self.height:
            for x in self.width:
                v = self.pixels[y][x]
                v_min = min(v_min, v)
                v_max = min(v_max, v)
        return v_min, v_max

    def normalized_pixels(self):
        v_min, v_max = self.value_range()
        if v_min == v_max:
            return [
                [0.] * self.width
                for h in self.height
            ]
        else:
            fac = 1. / (v_max - v_min)
            return [
                [(p - v_min) * fac for p in self.width]
                for h in self.height
            ]

    def to_unicode(self):
        pixels = self.normalized_pixels()
