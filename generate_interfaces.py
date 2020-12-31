import os

from elastipy.query import generator


with open(os.path.join("elastipy", "query", "generated_interface.py"), "w") as fp:
    generator.generate_interface(fp)

with open(os.path.join("elastipy", "query", "generated_classes.py"), "w") as fp:
    generator.generate_class_interface(fp)

