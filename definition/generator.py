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


def generate_query_interface():
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


def generate_query_class_interface():
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
            super_class_name="Query",
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


def generate_aggregation_interface():
    code = HEADLINE + "\n" + TYPING_IMPORT + "\n\n"

    code += f"\nfrom .interface import AggregationInterfaceBase\n\n"

    code += f"class AggregationInterface(AggregationInterfaceBase):\n\n"

    code += f"{INDENT}AGGREGATION_DEFINITION = {repr(AGGREGATION_DEFINITION)}\n"

    for agg_name in sorted(AGGREGATION_DEFINITION):
        definition = AGGREGATION_DEFINITION[agg_name]

        # TODO: how to nicely handle nested parameter values
        definition["parameters"] = {
            param_name.replace('.', '__'): param
            for param_name, param in definition["parameters"].items()
        }

        agg_type = {"bucket": "agg"}.get(definition["group"], definition["group"])

        # --- call generic function ---

        body = f"return self.{agg_type}(\n"
        body += f"{INDENT}*(aggregation_name + (\"{agg_name}\", )),\n"
        for param_name, param in definition["parameters"].items():
            body += f"{INDENT}{param_name}={param_name},\n"
        body += f")\n"

        code += render_function(
            function_name=f"{agg_type}_{agg_name}",
            parameters={
                "self": {},
                "*aggregation_name": {"type": "str", "doc": "Optional name to give the aggregation. "
                                                            "Otherwise it will be auto-generated"},
                **definition["parameters"]
            },
            doc=doc_with_url(definition),
            body=body,
            return_type="AggregationInterface",
            return_doc="A new instance is created and attached to the previous instance",
            indent=INDENT,
        ) + "\n"

    return code.rstrip() + "\n"



def generate_file(filename, func):
    with open(filename, "w") as fp:
        func(fp)
    print("written", filename)


if __name__ == "__main__":
    generate_file(
        os.path.join("elastipy", "query", "generated_interface.py"),
        generate_query_interface,
    )

    generate_file(
        os.path.join("elastipy", "query", "generated_classes.py"),
        generate_query_class_interface,
    )

    generate_file(
        os.path.join("elastipy", "aggregation", "generated_interface.py"),
        generate_aggregation_interface,
    )
