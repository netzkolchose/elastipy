import json
from typing import Union, TextIO

from .search import Response


class ResponseDump:

    def __init__(self, response: Response):
        self._response = response

    def __call__(self, indent: Union[int, str, None] = 2, file: TextIO = None):
        """
        Print the complete response.

        :param indent: The json indentation, defaults to 2.
        :param file: Optional output stream.
        """
        print(json.dumps(self._response, indent=indent), file=file)

    def documents(self, indent: Union[int, str, None] = 2, file: TextIO = None):
        """
        Print the list of documents inside the hits.

        :param indent: The json indentation, defaults to 2.
        :param file: Optional output stream.
        """
        print(json.dumps(self._response.documents, indent=indent), file=file)

    def aggregations(self, indent: Union[int, str, None] = 2, file: TextIO = None):
        """
        Print the aggregations part of the response.

        :param indent: The json indentation, defaults to 2.
        :param file: Optional output stream.
        """
        print(json.dumps(self._response.aggregations, indent=indent), file=file)

    def table(
            self,
            score: bool = True,
            sort: str = None,
            digits: int = None,
            header: bool = True,
            bars: bool = True,
            zero: Union[bool, float] = True,
            colors: bool = True,
            ascii: bool = False,
            max_width: int = None,
            max_bar_width: int = 40,
            file=None
    ):
        """
        Print the hit documents as a table.

        :param score: ``bool``
            Include the score for each hit

        :param sort: ``str``
            Optional sort column name which must match a 'header' key.
            Can be prefixed with ``-`` (minus) to reverse order

        :param digits: ``int``
            Optional number of digits for rounding.

        :param header: ``bool``
            if True, include the names in the first row.

        :param bars: ``bool``
            Enable display of horizontal bars in each number column.
            The table width will stretch out in size while limited
            to 'max_width' and 'max_bar_width'

        :param zero:
            - If ``True``: the bar axis starts at zero
              (or at a negative value if appropriate).
            - If ``False``: the bar starts at the minimum of all values in the column.
            - If a **number** is provided, the bar starts there,
              regardless of the minimum of all values.

        :param colors: ``bool``
            Enable console colors.

        :param ascii: ``bool``
            If ``True`` fall back to ascii characters.

        :param max_width: ``int``
            Will limit the expansion of the table when bars are enabled.
            If left None, the terminal width is used.

        :param max_bar_width: ``int``
            The maximum size a bar should have

        :param file:
            Optional text stream to print to.
        """
        from elastipy.dump import Table

        docs = self._response.documents
        if score:
            for i, (s, doc) in enumerate(zip(self._response.scores, docs)):
                docs[i] = {
                    "_score": s,
                    **doc
                }

        table = Table(docs)
        table.print(
            sort=sort,
            digits=digits,
            header=header,
            bars=bars,
            zero=zero,
            colors=colors,
            ascii=ascii,
            max_width=max_width,
            max_bar_width=max_bar_width,
            file=file,
        )
