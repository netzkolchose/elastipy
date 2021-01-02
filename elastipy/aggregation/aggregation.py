import json
import datetime
from typing import Optional, List, Iterable, Union, Tuple, TextIO, Sequence
from warnings import warn

from .. import make_json_compatible
from .generated_interface import AggregationInterface


class Aggregation(AggregationInterface):
    """
    Aggregation definition and response parser.

    Do not create instances yourself,
    use the Query.aggregation() and Aggregation.aggregation() variants
    """

    _factory_class_map = dict()

    def __init_subclass__(cls, **kwargs):
        if "factory" not in kwargs or kwargs["factory"]:
            Aggregation._factory_class_map[cls._agg_type] = cls

    def __init__(self, search, name, type, params):
        from ..search import Response
        from .visitor import AggregationVisitor
        AggregationInterface.__init__(self, timestamp_field=search.timestamp_field)
        self.search = search
        self.name = name
        self.type = type
        self.definition = self.AGGREGATION_DEFINITION.get(self.type) or dict()
        self.params = {
            key: value
            for key, value in params.items()
            if not self.definition.get("parameters") \
                or key not in self.definition["parameters"] \
                or self.definition["parameters"][key].get("required") \
                or self.definition["parameters"][key].get("default") != value
        }
        self._response: Optional[Response] = None
        self.parent: Optional[Aggregation] = None
        self.root: Aggregation = self
        self.children: List[Aggregation] = []
        self._visitor: Optional[AggregationVisitor] = None

    def __repr__(self):
        return f"{self.__class__.__name__}('{self.name}', '{self.type}')"

    @property
    def visitor(self) -> 'AggregationVisitor':
        """
        Returns an AggregationVisitor attached to this aggregation
        :return: AggregationVisitor instance
        """
        from .visitor import AggregationVisitor
        if self._visitor is None:
            self._visitor = AggregationVisitor(self)
        return self._visitor

    @property
    def group(self) -> str:
        """
        Returns the name of the aggregation group.
        :return: str, either "bucket", "metric" or "pipeline"
        """
        if "group" not in self.definition:
            warn(f"Aggregation '{self.name}'/{self.type} has no definition, 'group' is unknown.")
        return self.definition.get("group") or None

    def is_bucket(self):
        if "group" not in self.definition:
            warn(f"Aggregation '{self.name}'/{self.type} has no definition, is_bucket() is unknown")
        return self.definition.get("group") == "bucket"

    def is_metric(self):
        if "group" not in self.definition:
            warn(f"Aggregation '{self.name}'/{self.type} has no definition, is_metric() is unknown")
        return self.definition.get("group") == "metric"

    def is_pipeline(self):
        if "group" not in self.definition:
            warn(f"Aggregation '{self.name}'/{self.type} has no definition, is_pipeline() is unknown")
        return self.definition.get("group") == "pipeline"

    #def is_single_bucket(self):
    #    if not self.definition:
    #        warn(f"Aggregation '{self.name}'/{self.type} has no definition, is_single_bucket() is unknown")
    #    return self.definition.get("single_bucket")

    def metrics(self):
        """
        Iterate through all contained metric aggregations
        :return: generator of Aggregation
        """
        for c in self.children:
            if c.is_metric():
                yield c

    def to_body(self):
        """
        Returns the part of the elasticsearch request body
        :return: dict
        """
        return make_json_compatible(self.params)

    def aggregation(self, *aggregation_name_type, **params) -> 'Aggregation':
        """
        Interface to create sub-aggregations.

        This is the generic, undocumented version.
        Use the agg_*, metric_* and pipeline_* methods for convenience.

        :param aggregation_name_type: one or two strings, meaning either "type" or "name", "type"
        :param params: all parameters of the aggregation function
        :return: Aggregation instance
        """
        if len(aggregation_name_type) == 1:
            name = f"a{len(self.search._aggregations)}"
            aggregation_type = aggregation_name_type[0]
        elif len(aggregation_name_type) == 2:
            name, aggregation_type = aggregation_name_type
        else:
            raise ValueError(f"Need to provide (aggregation_type) or (name, aggregation_type), got {aggregation_name_type}")

        agg = factory(
            search=self.search, name=name, type=aggregation_type, params=params
        )
        agg.parent = self
        agg.root = self.root
        self.children.append(agg)
        self.search._aggregations.append(agg)
        self.search._add_body(f"{self.body_path()}.aggregations.{name}.{aggregation_type}", agg.to_body())
        return agg

    def execute(self):
        """
        Executes the whole query with all aggregations
        :return: self
        """
        self.search.execute()
        return self

    @property
    def response(self) -> dict:
        """
        Returns the response object of the aggregation

        Only available for root aggregations!
        :return: dict
        """
        if self.parent:
            raise ValueError(f"Can not get response of sub-aggregation '{self.name}' ({self.type})")
        if not self._response:
            raise ValueError(f"Can not get response of aggregation '{self.name}' ({self.type}), "
                             f"search has not been executed")
        return self._response.aggregations[self.name]

    @property
    def buckets(self) -> Union[dict, list]:
        """
        Returns the buckets of the aggregation response

        Only available for bucket root aggregations!
        :return: dict or list
        """
        if self.parent:
            raise ValueError(f"Can not get buckets of sub-aggregation '{self.name}' (type {self.type}) "
                             f"directly, use keys() and values()")
        return self.response["buckets"]

    def keys(self, key_separator=None):
        """
        Iterates through all keys of this aggregation.

        For example, a top-level date_histogram would return all timestamps.

        For a nested bucket aggregation each key is a tuple of all parent keys as well.

        :param key_separator: str, optional separator to concat multiple keys into one string
        :return: generator
        """
        return self.visitor.keys(key_separator=key_separator)

    def values(self, default=None):
        """
        Iterates through all values of this aggregation.
        :param default: if not None any None-value will be replaced by this
        :return: generator
        """
        return self.visitor.values(default=default)

    def items(self, key_separator=None, default=None) -> Iterable[Tuple]:
        """
        Iterates through all key, value tuples.
        :param key_separator: str, optional separator to concat multiple keys into one string
        :param default: if not None any None-value will be replaced by this
        :return: generator
        """
        yield from zip(self.keys(key_separator=key_separator), self.values(default=default))

    def dict_rows(self) -> Iterable[dict]:
        """
        Iterates through all result values from this aggregation branch.

        This will include all parent aggregations (up to the root) and all children
        aggregations (including metrics).

        :return: generator of dict
        """
        return self.visitor.dict_rows()

    def rows(self, header=True) -> Iterable[Sequence]:
        return self.visitor.rows(header=header)

    def to_dict(self, key_separator=None, default=None) -> dict:
        """
        Create a dictionary from all key/value pairs.
        :param key_separator: str, optional separator to concat multiple keys into one string
        :param default: if not None any None-value will be replaced by this
        :return: dict
        """
        return {
            key: value
            for key, value in self.items(key_separator=key_separator, default=default)
        }

    def dump_dict(self, key_separator="|", default=None, indent=2, file=None):
        print(json.dumps(self.to_dict(key_separator=key_separator, default=default), indent=indent), file=file)

    def dump_table(self, header: bool = True, file: TextIO = None):
        """
        Print the result of the dict_rows() function as table to console.
        :param header: bool, if True, include the names in the first row
        :param file: optional text stream to print to
        """
        self.visitor.dump_table(header=header, file=file)

    def key_name(self) -> str:
        """
        Return default name of the bucket key field.

        Metrics return their parent's key
        :return: str
        """
        if self.is_metric() and self.parent:
            return self.parent.key_name()
        key_name = "key"
        # TODO: this should be configurable
        if self.type == "date_histogram":
            key_name = "key_as_string"
        return key_name

    def body_path(self) -> str:
        """
        Return the dotted path of this aggregation in the request body
        :return: str
        """
        if not self.parent:
            return f"aggregations.{self.name}"
        else:
            return f"{self.parent.body_path()}.aggregations.{self.name}"


def factory(search, name, type, params) -> Aggregation:
    """
    Creates an instance of the matching Aggregation sub-class
    :return: instance of (derived) Aggregation class
    """
    if type in Aggregation._factory_class_map:
        klass = Aggregation._factory_class_map[type]
        try:
            return klass(search, name, type, params)
        except TypeError as e:
            raise TypeError(f"{e} in class {klass.__name__}")

    return Aggregation(search, name, type, params)
