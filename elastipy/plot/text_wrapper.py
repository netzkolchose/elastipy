from ..aggregation import Aggregation
from .text.textplotter import TextPlotter


class TextPlotWrapper:

    def __init__(self, source: Aggregation):
        self.source = source
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
