import os
from typing import Sequence


class UnicodeCharacters:
    """
    https://unicode.org/charts/PDF/U2580.pdf

    also interesting: https://en.wikipedia.org/wiki/Box-drawing_character
    """
    quadrants = ("▖", "▘", "▝", "▗")
    quadrants3 = ("▙", "▛", "▜", "▟")
    quadrants2 = ("▞", "▚")
    block = "█"
    left8th = ("▏", "▎", "▍", "▌", "▋", "▊", "▉")
    bottom8th = ("▁", "▂", "▃", "▄", "▅", "▆", "▇")
    top = "▀"
    right = "▐"
    shade = ("░", "▒", "▓")
    line_hori = "─"
    line_vert = "│"
    line_cross = "┼"
    line_corners = ("└", "┌", "┐", "┘")


class AsciiCharacters:
    block = "#"
    left8th = (".", ":")
    bottom8th = ("_", "-")
    line_vert = "|"
    line_hori = "-"
    line_cross = "+"
    line_corners = ("\\", "/", "\\", "/")


class Characters:

    def __init__(self, ascii=False):
        klass = AsciiCharacters if ascii else UnicodeCharacters
        self.block = klass.block
        self.left8th = klass.left8th
        self.bottom8th = klass.bottom8th
        self.line_vert = klass.line_vert
        self.line_hori = klass.line_hori
        self.line_cross = klass.line_cross
        self.line_corners = klass.line_corners
        if klass is UnicodeCharacters:
            self.quadrants = klass.quadrants
            self.quadrants2 = klass.quadrants2
            self.quadrants3 = klass.quadrants3
            self.top = klass.top
            self.right = klass.right
            self.shade = klass.shade

    def hbar(self, v, width):
        """
        Return a string containing a horizontal bar
        :param v: float, in range [0, 1]
        :param width: int, number of characters
        :return: str
        """
        return self._bar(v, width, self.left8th)

    def _bar(self, v, width, characters):
        v = max(0., min(1., v))
        v = v * width
        v_floor = int(v)
        v_fract = v - int(v)
        num_char = len(characters)
        ret = self.block * v_floor
        if v_fract >= 1. / (num_char + 1):
            rest = int(v_fract * num_char)
            ret += characters[rest]
        return ret + " " * (width - len(ret))


class ColorScale:

    def __init__(self, ascii=False, colors=True, characters: Sequence[str] = None):
        self.characters = []
        if characters:
            self.characters = characters
        elif colors and not ascii:
            colors = [4, 6, 2, 7]

            intensity = 0 if is_notebook() else 1
            back_color = 0
            shades = ("░", "▒", "▓", "█")
            for i, color in enumerate(colors):
                for ch in shades:
                    ansi = f"\033[{intensity};{30+color};{40+back_color}m{ch}\033[0m"
                    self.characters.append(ansi)
                back_color = color
                if i == 0:
                    shades = shades[1:]
        elif colors and ascii:
            # TODO: add colors
            self.characters = [".", ":", "*", "#"]
        elif not colors and ascii:
            self.characters = ".:*#"
        else:  # not colors and not ascii:
            self.characters = ("░", "▒", "▓", "█")

    def __call__(self, v: float):
        i = max(0, min(len(self.characters) - 1, int(v * len(self.characters))))
        return self.characters[i]


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


# rene-d 2018 https://gist.github.com/rene-d/9e584a7dd2935d0f461904b9f2950007
class ColorCodes:
    """ ANSI color codes """
    BLACK = "\033[0;30m"
    RED = "\033[0;31m"
    GREEN = "\033[0;32m"
    BROWN = "\033[0;33m"
    BLUE = "\033[0;34m"
    PURPLE = "\033[0;35m"
    CYAN = "\033[0;36m"
    LIGHT_GRAY = "\033[0;37m"
    DARK_GRAY = "\033[1;30m"
    LIGHT_RED = "\033[1;31m"
    LIGHT_GREEN = "\033[1;32m"
    YELLOW = "\033[1;33m"
    LIGHT_BLUE = "\033[1;34m"
    LIGHT_PURPLE = "\033[1;35m"
    LIGHT_CYAN = "\033[1;36m"
    LIGHT_WHITE = "\033[1;37m"
    BOLD = "\033[1m"
    FAINT = "\033[2m"
    ITALIC = "\033[3m"
    UNDERLINE = "\033[4m"
    BLINK = "\033[5m"
    NEGATIVE = "\033[7m"
    CROSSED = "\033[9m"
    END = "\033[0m"


class Colors:
    def __init__(self, enable=True):
        self.BLACK = ColorCodes.BLACK if enable else ""
        self.RED = ColorCodes.RED if enable else ""
        self.GREEN = ColorCodes.GREEN if enable else ""
        self.BROWN = ColorCodes.BROWN if enable else ""
        self.BLUE = ColorCodes.BLUE if enable else ""
        self.PURPLE = ColorCodes.PURPLE if enable else ""
        self.CYAN = ColorCodes.CYAN if enable else ""
        self.LIGHT_GRAY = ColorCodes.LIGHT_GRAY if enable else ""
        self.DARK_GRAY = ColorCodes.DARK_GRAY if enable else ""
        self.LIGHT_RED = ColorCodes.LIGHT_RED if enable else ""
        self.LIGHT_GREEN = ColorCodes.LIGHT_GREEN if enable else ""
        self.YELLOW = ColorCodes.YELLOW if enable else ""
        self.LIGHT_BLUE = ColorCodes.LIGHT_BLUE if enable else ""
        self.LIGHT_PURPLE = ColorCodes.LIGHT_PURPLE if enable else ""
        self.LIGHT_CYAN = ColorCodes.LIGHT_CYAN if enable else ""
        self.LIGHT_WHITE = ColorCodes.LIGHT_WHITE if enable else ""
        self.BOLD = ColorCodes.BOLD if enable else ""
        self.FAINT = ColorCodes.FAINT if enable else ""
        self.ITALIC = ColorCodes.ITALIC if enable else ""
        self.UNDERLINE = ColorCodes.UNDERLINE if enable else ""
        self.BLINK = ColorCodes.BLINK if enable else ""
        self.NEGATIVE = ColorCodes.NEGATIVE if enable else ""
        self.CROSSED = ColorCodes.CROSSED if enable else ""
        self.END = ColorCodes.END if enable else ""


def get_terminal_size():
    """
    Return size of terminal.

    If running in a notebook it returns some default values
    which fit at least on my local setup..

    :return: tuple(int, int) width and height
    """
    if is_notebook():
        return 110, 30

    w, h = os.get_terminal_size()
    return w, h


def is_notebook() -> bool:
    """
    Returns True if inside ipython notebook, False otherwise.

    See lengthy discussion: https://stackoverflow.com/questions/15411967/how-can-i-check-if-code-is-executed-in-the-ipython-notebook
    :return: bool
    """
    try:
        name = type(get_ipython()).__name__
        return name == "ZMQInteractiveShell"
    except NameError:
        return False


def clip_line(line, max_width=None):
    if max_width is None:
        return line

    return line

    # TODO: this is currently not working when colors are involved
    if len(line) > max_width > 2:
        line, rest = line[:max_width-2], line[max(0, max_width - 2 - len(ColorCodes.END)):]
        if ColorCodes.END in rest:
            line += ColorCodes.END
        line += ".."

    return line
