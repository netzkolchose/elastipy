import re
from typing import Union

from .markd import parse_markdown

INDENT = "    "


# detect markdown links
MARKDOWN_LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
# detect single `literals`
MARKDOWN_LITERALS_RE = re.compile(r"`+([^`]+)`+")


def doc_to_rst(text):
    text = parse_markdown(text)
    text = sections_to_rst(text)
    text = "\n".join("" if not line.strip() else line for line in text.splitlines())
    return text


def is_bullet_line(line: str) -> bool:
    return line.lstrip().startswith("- ")


def sections_to_rst(text: str) -> str:
    """
    Replace a simple 'Note: blabla' with the rst equivalent.
    TODO: Does not care too much for indentation and existing blocks,
        it just works a.t.m.
    """
    for word, rst_section in (
            ("Note", "NOTE"),
            ("Warning", "WARNING"),
            ("Important", "IMPORTANT"),
            ("Code", "CODE"),
    ):
        text = text.replace(f"{word}: ", f".. {rst_section}::\n\n    ")
        text = text.replace(f"{word}:", f".. {rst_section}::\n   ")
    return text


def type_to_str(param):
    if isinstance(param, str):
        if "Interface" in param and "'" not in param:
            return f"'{param}'"
        return param

    type = param.get("type")
    if not type:
        return None
    if isinstance(type, (list, tuple)):
        types = [type_to_str(t) for t in type]
    else:
        types = [type_to_str(type)]

    if not param.get("required") and param.get("default") is None and None not in types:
        types.append(None)

    if len(types) > 1:
        if len(types) == 2 and None in types:
            type = types[0] or types[1]
            return f"Optional[{type}]"
        return f"Union[{', '.join(map(str, types))}]"

    return types[0]


def render_function(
        function_name, parameters, doc, body,
        return_type=None, return_doc=None, annotate_return_type=True, indent="",
        with_doc_types: bool = True,
):
    # -- definition --

    code = f"def {function_name}(\n"
    for param_name, param in parameters.items():
        param_str = param_name

        if type_to_str(param):
            param_str += f": {type_to_str(param)}"

        if not param.get("required") and param_name != "self" and not param_name.startswith("*"):
            param_str += " = " + repr(param.get("default"))
        code += f"{INDENT}{INDENT}{param_str},\n"
    code += f")"

    if return_type is not None and annotate_return_type:
        code += f" -> {type_to_str(return_type)}"

    code += ":\n"

    # --- doc string ---

    code += f'{INDENT}"""\n'
    if doc:
        code += change_text_indent(doc_to_rst(doc), INDENT, max_length=80) + "\n"

    for param_name, param in parameters.items():
        if param_name != "self":
            code += f"\n{INDENT}:param {param_name.lstrip('*')}:"
            if with_doc_types:
                code += f" ``{type_to_str(param)}``\n"
            else:
                code += "\n"
            param_doc = get_param_doc(param)
            if param_doc:
                code += change_text_indent(doc_to_rst(param_doc), INDENT*2, max_length=80) + "\n"

    if return_type:
        code += f"\n{INDENT}:returns: ``{type_to_str(return_type)}``\n"
        if return_doc:
            code += change_text_indent(doc_to_rst(return_doc), INDENT*2, max_length=80) + "\n"

    code += f'{INDENT}"""\n'

    # --- body ---

    code += change_text_indent(body, INDENT)

    if indent:
        code = change_text_indent(code, indent)

    return code.rstrip() + "\n"


def render_class(class_name, super_class_name, class_parameters, doc=None, functions=None, indent=""):
    code = f"class {class_name}({super_class_name}):\n\n"

    if doc:
        code += change_text_indent(f'"""\n{doc_to_rst(doc.rstrip())}\n"""', INDENT, max_length=80) + "\n"

    if class_parameters:
        code += "\n"
        for param_name, param in class_parameters.items():
            code += f"{INDENT}{param_name} = {repr(param)}\n"
        code += "\n"

    if indent:
        code = change_text_indent(code, indent)

    if functions:
        for f in functions:
            code += "\n" + render_function(**f, indent=INDENT)

    return code.rstrip() + "\n"


def change_text_indent(text: str, indent: Union[str, int] = 0, max_length=None) -> str:
    """
    Changes the indentation of a block of text.
    All leading whitespace on each line is stripped up to the
    maximum common length of ws for each line and then 'len' spaces are inserted.
    Also merges multiple new-lines into one

    :param text: str, the text to change
    :param indent: int|str, Number of spaces to have in front
    :param max_length: int|None, Number of maximum columns to occupy or None for unlimited
    :return: str
    """
    if not isinstance(indent, int):
        indent = len(indent)

    lines = text.replace("\t", INDENT).split("\n")
    while lines and not lines[0].strip():
        lines = lines[1:]
    while lines and not lines[-1].strip():
        lines = lines[:-1]

    if not lines:
        return ""
    min_space = min(len(line) - len(line.lstrip()) for line in lines)

    pre = " " * indent
    text = ""
    was_nl = False
    was_bullet = False
    for line in lines:
        li = line[min_space:]
        if li:
            if not max_length:
                text += pre + li + "\n"
            else:
                if li.lstrip().startswith("- "):
                    was_bullet = True
                text += break_line(pre, li, max_length, was_bullet) + "\n"
            was_nl = False
        else:
            if not was_nl:
                text += "\n"
            was_nl = True
            was_bullet = False

    if text.endswith("\n"):
        text = text[:-1]

    return text


def break_line(pre: str, line: str, max_length: int, is_bullet: bool) -> str:
    # print(f"BREAK [{pre}] [{line}]")

    text = ""
    add_pre = len(line) - len(line.lstrip())
    line = line[add_pre:]

    pre += " " * add_pre
    bullet_pre = pre + "  "

    while line:
        line_part = line
        new_line = (bullet_pre if is_bullet and not is_bullet_line(line_part) else pre) + line_part
        while len(new_line) > max_length:
            try:
                space_idx = line_part.rindex(" ")
            except ValueError:
                break
            if not space_idx:
                break
            line_part = line_part[:space_idx]
            new_line = (bullet_pre if is_bullet and not is_bullet_line(line_part) else pre) + line_part

        if text:
            text += "\n"
        text += new_line.rstrip()
        line = line[len(line_part)+1:]

    return text


def get_param_doc(param):
    doc = param.get("doc") or ""
    if param.get("timestamp"):
        if doc:
            doc += "\n\n"
        doc += """If no field is specified it will default to the 'timestamp_field' of the Search class.\n"""

    return doc.rstrip() + "\n"


if __name__ == "__main__":

    print(render_function(
        function_name="some_function",
        parameters={
            "a": {"type": "str", "required": True},
            "b": {"doc": "Some\n\nDoc!"},
            "c": {}
        },
        doc="Description of function\n\nwith breaks",
        body="pass"
    ))
    print("-"*40)
    print(render_class(
        class_name="SomeClass",
        super_class_name="SomeSuperClass",
        class_parameters={
            "class_attribute": 23,
        },
        doc="Documentation!",
        functions=[
            dict(
                function_name="some_function",
                parameters={
                    "a": {"type": "str", "required": True},
                    "b": {"doc": "Some\n\nDoc!"},
                    "c": {}
                },
                doc="Description of function\n\nwith breaks",
                body="pass"
            )
        ],
    ))