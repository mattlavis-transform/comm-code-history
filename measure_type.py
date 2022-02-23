import os
from classes.sqlite_helper import DatabaseLite
from strings import Strings


class MeasureType(object):
    def __init__(self):
        pass

    def as_dict(self):
        ret = {
            "id": self.measure_type_id,
            "type": "measure_type",
            "attributes": {
                "id": self.measure_type_id,
                "description": self.description
            }
        }
        return ret
    