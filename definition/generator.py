import os
import datetime

from .data import QUERY_DEFINITION, AGGREGATION_DEFINITION
from .renderer import render_function, render_class, change_text_indent


INDENT = "    "
HEADLINE = f"# auto-generated file - do not edit"
TYPING_IMPORT = "from typing import Mapping, Sequence, Any, Union, Optional"


def doc_with_url(definition):
    doc = definition.get("doc")
    if definition.get("url"):
        if not doc:
            doc = ""
        doc += f"\n{definition['url']}"

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


def render_query_classes():
    code = HEADLINE + "\n" + TYPING_IMPORT + "\n\n"

    code += f"\nfrom .query import Query, QueryInterface\n\n"

    for query_name in sorted(QUERY_DEFINITION):
        definition = QUERY_DEFINITION[query_name]

        class_name = "".join(p.title() for p in query_name.split("_"))
        if definition.get("base_class"):
            class_name = f"_{class_name}"

        class_parameters = {
            "name": query_name,
            "_optional_parameters": {
                param_name: param.get("default")
                for param_name, param in definition["parameters"].items()
                if not param.get("required")
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
            super_class_name="Query, factory=False" if definition.get("base_class") else "Query",
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
            short_param = {
                "type": param["type"],
            }
            for key in ("required", "default"):
                if key in param:
                    short_param[key] = param[key]
            short_agg["parameters"][param_name] = short_param
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

        do_return_parent = False  #definition["group"] == "metric"

        body = f"agg = self.{agg_type}(\n"
        body += f"{INDENT}*(aggregation_name + (\"{agg_name}\", )),\n"
        for param_name, param in definition["parameters"].items():
            body += f"{INDENT}{param_name}={param_name},\n"
        body += f")\n"
        body += "return self\n" if do_return_parent else "return agg\n"

        code += render_function(
            function_name=f"{agg_type}_{agg_name}",
            parameters={
                "self": {},
                "*aggregation_name": {"type": "str", "doc": "Optional name of the aggregation. "
                                                            "Otherwise it will be auto-generated."},
                **definition["parameters"]
            },
            doc=doc_with_url(definition),
            body=body,
            return_type="AggregationInterface",
            return_doc="A new instance is created and attached to the parent, the %s is returned." % (
                "parent" if do_return_parent else "new instance"
            ),
            annotate_return_type=False,
            indent=INDENT,
        ) + "\n"

    return code.rstrip() + "\n"