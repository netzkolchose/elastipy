"""
Currently collection of all queries that have some peculiarity
"""

from .generated_classes import _Terms


class Terms(_Terms):

    def to_dict(self):
        # the 'field' parameter is not mentioned by key but by actually value
        dic = {
            self.parameters["field"]: self.parameters["value"]
        }
        if self.parameters.get("boost"):
            dic["boost"] = self.parameters["boost"]

        return {self.name: dic}
