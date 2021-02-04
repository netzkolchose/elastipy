import re
from typing import Tuple, Union, List, Optional
from docutils import nodes
from docutils.parsers.rst import Directive
from sphinx.roles import XRefRole


def get_external_link(target: str) -> Optional[str]:
    if target.startswith("pandas."):
        return f"https://pandas.pydata.org/pandas-docs/stable/reference/api/{target}.html"
    if target.endswith("matplotlib.axes.Axes"):
        return "https://matplotlib.org/3.3.3/api/axes_api.html#the-axes-class"


INTERNAL_CLASS_LINKS = [
    ("elastipy.aggregation.aggregation_dump.AggregationDump", "reference/aggregation"),
    ("elastipy.aggregation.Aggregation", "reference/aggregation"),
    ("elastipy.Search", "reference/search"),
    ("elastipy.Exporter", "reference/exporter"),
    ("elastipy.aggregation.aggregation_plot_pd.PandasPlotWrapper", "reference/aggregation"),
]


def get_internal_link(target: str) -> Tuple[str, str]:
    for class_path, doc_path in INTERNAL_CLASS_LINKS:
        class_name = class_path.split(".")[-1]
        if target.startswith(class_name):
            return doc_path, class_path + target[len(class_name):]
            #return f"{doc_path}.html#{class_path}" + target[len(class_name):]

    return "", ""
    #for r, path in INTERNAL_LINK_RE:
    #    match = r.match(target)
    #    if match:
    #        return f"{path}.html#{match.group(0)}"


def relative_path_change(
        own_path: Union[str, List[str]],
        other_path: Union[str, List[str]],
        separator: str = "/") -> str:
    """
    Convert one absolute path to another absolute path
    using relative path (..) syntax.

    :param own_path: str or list[str]
    :param other_path: str or list[str]
    :param separator: str
    :return: str
    """
    if isinstance(own_path, str):
        own_path = own_path.split(separator) if own_path else []
    if isinstance(other_path, str):
        other_path = other_path.split(separator) if other_path else []

    if own_path == other_path:
        return ""
    elif not own_path and other_path:
        return separator.join(other_path)
    elif own_path and not other_path:
        return separator.join(".." for _ in own_path)
    else:
        own_path = own_path.copy()
        other_path = other_path.copy()
        while own_path and other_path and own_path[0] == other_path[0]:
            own_path.pop(0)
            other_path.pop(0)

        if not own_path and other_path:
            return separator.join(other_path)
        elif own_path and not other_path:
            return separator.join(".." for _ in own_path)

        path = [".." for _ in own_path]
        path += other_path
        return separator.join(path)


class LinkRole(XRefRole):

    def get_link_uri(self, target):
        if target.endswith("()"):
            target = target[:-2]

        doc_path, node_id = None, None
        for key, value in self.env.domaindata["py"]["objects"].items():
            if key.endswith(target):
                obj = value
                doc_path = obj.docname
                node_id = obj.node_id

        if not doc_path:
            doc_path, node_id = get_internal_link(target)

        if not doc_path:
            uri = get_external_link(target)
            if uri:
                return uri

        if not doc_path:
            keys = self.env.domaindata["py"]["objects"].keys()
            raise ValueError(
                f":link: not found '{target}', in {keys}"
            )

        own_path = self.env.docname.split("/")
        doc_path = doc_path.split("/")
        own_path, own_file = own_path[:-1], own_path[-1]
        doc_path, doc_file = doc_path[:-1], doc_path[-1]

        uri = relative_path_change(own_path, doc_path)
        if uri:
            uri += "/"
        uri += f"{doc_file}.html#{node_id}"

        return uri

    def run(self):
        res = super().run()
        node = nodes.reference(refuri=self.get_link_uri(self.target))

        node.append(res[0][0])
        return [node], []


def setup(app):
    app.add_role("link", LinkRole(), override=True)

    return {
        'version': '0.1',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }


def dump_obj(obj, path=(), exclude=None, max_depth=10):
    """Some debugging tool"""
    import inspect

    if exclude is None:
        exclude = set()

    try:
        if obj in exclude:
            return
        exclude.add(obj)
    except TypeError:
        pass

    if len(path) > max_depth:
        print(".".join(path), obj)
        return

    if isinstance(obj, dict):
        for key, value in obj.items():
            dump_obj(value, path+(str(key), ), exclude, max_depth)

    elif isinstance(obj, (list, tuple)):
        for key, value in enumerate(obj):
            dump_obj(value, path+(str(key), ), exclude, max_depth)

    elif isinstance(obj, (int, str, float, bool)) or inspect.ismodule(obj):
        print(".".join(path), obj)

    elif isinstance(obj, object):
        for key in dir(obj):
            if not key.startswith("__") and hasattr(obj, key):
                try:
                    dump_obj(getattr(obj, key), path + (key,), exclude, max_depth)
                except:
                    pass
    else:
        print(".".join(path), obj)
