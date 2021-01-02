import os

from definition import generator


def generate_file(filename, text):
    with open(filename, "w") as fp:
        fp.write(text)
    print(f"written {len(text)//1024}kb to {filename}")


if __name__ == "__main__":
    generate_file(
        os.path.join("elastipy", "query", "generated_interface.py"),
        generator.generate_query_interface(),
    )

    generate_file(
        os.path.join("elastipy", "query", "generated_classes.py"),
        generator.generate_query_class_interface(),
    )

    generate_file(
        os.path.join("elastipy", "aggregation", "generated_interface.py"),
        generator.generate_aggregation_interface(),
    )

