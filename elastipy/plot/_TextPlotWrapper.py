import os

from .._Aggregation import Aggregation
from ._TextPlotter import TextPlotter


class TextPlotWrapper:

    def __init__(self, source):
        self.source: Aggregation = source
        self.plotter = TextPlotter()

    def hbar(self, width=None, zero_based=True, digits=3, file=None):
        keys = list(self.source.keys(key_separator="|"))
        values = list(self.source.values())
        self.plotter.hbar(
            keys=keys,
            values=values,
            width=width,
            zero_based=zero_based,
            digits=digits,
            file=file,
        )
