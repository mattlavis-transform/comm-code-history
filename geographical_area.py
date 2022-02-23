import os
from classes.sqlite_helper import DatabaseLite
from strings import Strings


class GeographicalArea(object):
    def __init__(self):
        pass

    def as_dict(self):
        ret = {
            "id": self.geographical_area_id,
            "type": "geographical_area",
            "attributes": {
                "id": self.geographical_area_id,
                "description": self.description,
                "geographical_area_id": self.geographical_area_id
            }
        }
        return ret
    