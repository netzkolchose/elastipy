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

    return data


QUERY_DEFINITION = import_yamls("query")
AGGREGATION_DEFINITION = import_yamls("aggregation")

assert QUERY_DEFINITION, "Definition not loaded"
assert AGGREGATION_DEFINITION, "Definition not loaded"
