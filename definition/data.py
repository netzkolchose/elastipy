import pathlib
import yaml


def import_yamls(main_dir: str):
    data = dict()
    path = pathlib.Path(pathlib.Path(__file__).parent.resolve(), main_dir)
    for group_path in path.glob("*"):
        if group_path.is_dir() and "pycache" not in str(group_path):
            for yaml_file in group_path.glob("*.yaml"):
                yaml_data = yaml.safe_load(yaml_file.read_text())
                yaml_data["group"] = group_path.name
                data.update({yaml_file.name[:-5]: yaml_data})

    return {
        key: data[key]
        for key in sorted(data)
    }


def import_search_yamls(main_dir: str):
    data = dict()
    path = pathlib.Path(pathlib.Path(__file__).parent.resolve(), main_dir)
    for yaml_file in path.glob("*.yaml"):
        group = yaml_file.name[:-5]
        yaml_data = yaml.safe_load(yaml_file.read_text())
        for param in yaml_data["parameters"].values():
            param["group"] = group
        data[group] = yaml_data

    assert "body" in data
    assert "query" in data

    ret_data = {
        **data["query"]["parameters"],
        # body params replace query params as they are generally
        # more versatile
        **data["body"]["parameters"],
    }

    return {
        key: ret_data[key]
        for key in sorted(ret_data)
    }


QUERY_DEFINITION = import_yamls("query")
AGGREGATION_DEFINITION = import_yamls("aggregation")
SEARCH_PARAM_DEFINITION = import_search_yamls("search")

assert QUERY_DEFINITION, "Definition not loaded"
assert AGGREGATION_DEFINITION, "Definition not loaded"
assert SEARCH_PARAM_DEFINITION, "Definition not loaded"
