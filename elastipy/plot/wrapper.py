from ..aggregation import Aggregation


class PlotWrapper:

    def __init__(self, source: Aggregation):
        self.source = source
        self._wrapper = dict()

    @property
    def text(self):
        from .text_wrapper import TextPlotWrapper
        if "text" not in self._wrapper:
            self._wrapper["text"] = TextPlotWrapper(self.source)
        return self._wrapper["text"]
