from .data import QUERY_DEFINITION, AGGREGATION_DEFINITION, SEARCH_PARAM_DEFINITION
from .renderer import render_function, render_class, change_text_indent


INDENT = "    "
HEADLINE = f"# auto-generated file - do not edit"
TYPING_IMPORT = """
from datetime import date, datetime
from typing import Mapping, Sequence, Any, Union, Optional
""".strip()


def doc_with_url(definition):
    doc = definition.get("doc")
    if definition.get("url"):
        if not doc:
            doc = ""
        doc += f"\n[elasticsearch documentation]({definition['url']})"

    return doc


def render_query_class():
    code = HEADLINE + "\n" + TYPING_IMPORT + "\n\n"

    code += f"\nfrom .interface import QueryInterfaceBase\n\n"

    code += f"class QueryInterface(QueryInterfaceBase):\n\n"

    for query_name in sorted(QUERY_DEFINITION):
        definition = QUERY_DEFINITION[query_name]

        body = f"return self.add_query(\n"
        body += f"{INDENT}\"{query_name}\",\n"
        for param_name, param in definition["parameters"].items():
            body += f"{INDENT}{param_name}={param_name},\n"
        body += f")\n"

        code += render_function(
            function_name=query_name,
            parameters={"self": {}, **definition["parameters"]},
            doc=doc_with_url(definition),
            body=body,
            return_type="QueryInterface",
            return_doc="A new instance is created",
            indent=INDENT,
        ) + "\n"

    return code.rstrip() + "\n"


def to_class_name(name, abstract=False):
    class_name = "".join(p.title() for p in name.split("_"))
    if abstract:
        class_name = f"_{class_name}"
    return class_name


def render_query_classes():
    code = HEADLINE + "\n" + TYPING_IMPORT + "\n\n"

    code += f"from .query import Query, QueryInterface\n\n"

    export_names = tuple(
        to_class_name(query_name, QUERY_DEFINITION[query_name].get("abstract"))
        for query_name in sorted(QUERY_DEFINITION)
    )

    code += f"\n__all__ = (\n"
    code += change_text_indent(", ".join(f'"{n}"' for n in export_names), INDENT, max_length=80)
    code += "\n)\n\n"

    for query_name in sorted(QUERY_DEFINITION):
        definition = QUERY_DEFINITION[query_name]

        class_name = to_class_name(query_name, definition.get("abstract"))

        class_parameters = {
            "name": query_name,
            "_parameters": {
                param_name: {
                    key: value
                    for key, value in param.items()
                    if key not in ("doc", "type")
                }
                for param_name, param in definition["parameters"].items()
            }
        }

        for param_name, param in definition["parameters"].items():
            if param.get("top_level"):
                class_parameters["_top_level_parameter"] = param_name

        body = f"super().__init__(\n"
        for param_name, param in definition["parameters"].items():
            body += f"{INDENT}{param_name}={param_name},\n"
        body += f")\n"

        code += "\n" + render_class(
            class_name=class_name,
            super_class_name="Query, factory=False" if definition.get("abstract") else "Query",
            class_parameters=class_parameters,
            doc=doc_with_url(definition),
            functions=[
                dict(
                    function_name="__init__",
                    parameters={"self": {}, **(definition.get("parameters") or {})},
                    doc=doc_with_url(definition),
                    body=body,
                )
            ],
        ) + "\n"

    return code


def render_aggregation_class():
    code = HEADLINE + "\n" + TYPING_IMPORT + "\n\n"

    code += f"from .interface import AggregationInterfaceBase\n\n\n"

    code += f"class AggregationInterface(AggregationInterfaceBase):\n\n"

    # stripped-down version of the definition to access at class level
    short_definition = dict()
    for agg_name, agg in AGGREGATION_DEFINITION.items():
        short_agg = {
            "group": agg["group"],
            "parameters": dict(),
        }
        for key in ("returns", ):
            if key in agg:
                short_agg[key] = agg[key]
        for param_name, param in agg["parameters"].items():
            short_agg["parameters"][param_name] = {
                key: value
                for key, value in param.items()
                if key != "doc"
            }
        short_definition[agg_name] = short_agg

    code += f"{INDENT}AGGREGATION_DEFINITION = {repr(short_definition)}\n\n"

    # -- class method for each aggregation

    for agg_name in sorted(AGGREGATION_DEFINITION):
        definition = AGGREGATION_DEFINITION[agg_name]

        # TODO: how to nicely handle nested parameter values
        definition["parameters"] = {
            param_name.replace('.', '__'): param
            for param_name, param in definition["parameters"].items()
        }

        agg_type = {"bucket": "agg"}.get(definition["group"], definition["group"])

        # --- call generic function ---

        do_return_parent = definition["group"] in ("metric", "pipeline")

        extra_parameters = {}
        return_doc = "A new instance is created and returned"
        if do_return_parent:
            return_doc = "A new instance is created and attached to the parent and the parent is returned, " \
                         "unless 'return_self' is True, in which case the new instance is returned."
            extra_parameters["return_self"] = {
                "type": "bool",
                "default": False,
                "doc": f"If True, this call returns the created "
                       f"{definition['group']}, otherwise the parent is returned.",
            }
            for key in extra_parameters:
                assert key not in definition["parameters"], \
                    f"Unfortunately, the elastipy parameter '{key}' is already present in the parameters of " \
                    f"aggregation '{agg_name}'"

        # -- method body --
        #body = "from .aggregation import Aggregation"
        body = f"a = self.{agg_type}(\n"
        body += f"{INDENT}*(aggregation_name + (\"{agg_name}\", )),\n"
        for param_name, param in definition["parameters"].items():
            body += f"{INDENT}{param_name}={param_name},\n"
        if do_return_parent:
            body += f"{INDENT}return_self=return_self,\n"
        body += f")\n"
        body += f"return a\n"
        #if do_return_parent:
        #    body += "return agg if return_self else self\n"
        #else:
        #    body += "a\n"

        code += render_function(
            function_name=f"{agg_type}_{agg_name}",
            parameters={
                "self": {},
                "*aggregation_name": {"type": "str", "doc": "Optional name of the aggregation. "
                                                            "Otherwise it will be auto-generated."},
                **definition["parameters"],
                **extra_parameters,
            },
            doc=doc_with_url(definition),
            body=body,
            return_type="AggregationInterface",
            return_doc=return_doc,
            annotate_return_type=False,
            indent=INDENT,
        ) + "\n"

    return code.rstrip() + "\n"


def render_search_param_class():
    code = HEADLINE + "\n" + TYPING_IMPORT + "\n\n"
    code += "from .search_param import SearchParametersBase\n"
    code += "from .search import Search\n\n"

    code += f"\nclass Unset:\n{INDENT}pass\n\n"

    code += f"\nclass SearchParameters(SearchParametersBase):\n\n"

    code += f"{INDENT}# make sure sphinx get's the documentation string\n"
    code += f"{INDENT}__doc__ = SearchParametersBase.__doc__\n\n"

    # stripped-down version of the definition to access at class level
    short_definition = dict()
    for param_name, param in SEARCH_PARAM_DEFINITION.items():
        short_definition[param_name] = {
            key: value
            for key, value in param.items()
            if key not in ("doc", "type")
        }

    code += f"{INDENT}DEFINITION = {repr(short_definition)}\n\n"

    # -- combined method for all parameters --

    COMBINED_DOC = change_text_indent("""
        Can set all search parameters at once.
        
        Each parameter that is different than it's
        default value is put into the search request.
        
        For elasticsearch below version 8,
        the parameters are automatically split into 
        query and body representation. 
    """)

    def func_name(name):
        func_name = name.lstrip('_')
        func_name = {"from": "from_"}.get(func_name, func_name)
        return func_name

    combined_params = dict()
    combined_body = "s = self._search.copy()\n"
    for name, defi in SEARCH_PARAM_DEFINITION.items():
        fname = func_name(name)
        #combined_body += f"if {fname} != self.DEFINITION[\"{name}\"].get(\"default\")
        combined_body += f"if {fname} is not Unset:\n"
        combined_body += f"{INDENT}s._parameters._params[\"{name}\"] = {fname}\n"

        defi = defi.copy()
        # defi["type"] = f"Union[Type[Unset], {defi['type']}]"
        defi["declaration_default"] = "Unset"
        combined_params[fname] = defi
    combined_body += "return s\n"

    code += render_function(
        function_name="__call__",
        parameters={
            "self": {},
            **combined_params,
        },
        doc=COMBINED_DOC,
        body=combined_body,
        return_type="Search",
        return_doc="A new Search instance is created",
        annotate_return_type=True,
        indent=INDENT,
    ) + "\n"

    # -- method for each search parameter ---

    for param_name, definition in SEARCH_PARAM_DEFINITION.items():

        # -- method body --
        body = f"return self._set_parameter(\"{param_name}\", value)\n"

        code += render_function(
            function_name=f"{func_name(param_name)}",
            parameters={
                "self": {},
                "value": {
                    **definition
                },
            },
            doc=f"A search **{definition['group']}** parameter.",
            body=body,
            return_type="Search",
            return_doc="A new Search instance is created",
            annotate_return_type=True,
            indent=INDENT,
        ) + "\n"

    return code.rstrip() + "\n"


def render_rst_agg_index():
    code = ""

    groups = sorted(set(d["group"] for d in AGGREGATION_DEFINITION.values()))
    for group in groups:
        code += f"- {group}\n\n"
        for agg_name in sorted(filter(lambda key: AGGREGATION_DEFINITION[key]["group"] == group, AGGREGATION_DEFINITION)):
            definition = AGGREGATION_DEFINITION[agg_name]
            group = {"bucket": "agg"}.get(definition["group"], definition["group"])
            code += f"  - `{agg_name} <#elastipy.aggregation.Aggregation.{group}_{agg_name}>`__\n"
        code += "\n"

    return code


def render_rst_query_index():
    code = ""

    groups = sorted(set(d["group"] for d in QUERY_DEFINITION.values()))
    for group in groups:
        code += f"- {group}\n\n"
        for query_name in sorted(filter(lambda key: QUERY_DEFINITION[key]["group"] == group, QUERY_DEFINITION)):
            definition = QUERY_DEFINITION[query_name]
            code += f"  - `{query_name} <#elastipy.Search.{query_name}>`__\n"
        code += "\n"

    return code
