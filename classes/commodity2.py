from datetime import datetime
from classes.database import Database
from classes.sqlite_helper import DatabaseLite
import os


class Commodity2(object):
    def __init__(self, commodity_code):
        self.commodity_code = commodity_code
        self.get_date_sql_lite()

    def get_date_sql_lite(self):
        self.data = {}
        self.instances = []
    
        instance = {
            "sid": 1,
            "goods_nomenclature_item_id": "test",
            "validity_start_date": "test",
            "validity_end_date": "test",
            "validity_start_date_display": "test",
            "validity_end_date_display": "test"
        }
        self.instances.append(instance)
            
        self.data["data"] = self.instances

    def to_yyyymmdd(self, s):
        if s is None:
            s = ""
        else:
            if isinstance(s, str):
                s = datetime.strptime(s, "%Y-%m-%d %H:%M:%S")
            
            s = datetime.strftime(s, "%Y-%m-%d")
        return s
        
    def to_display(self, s):
        if s is None:
            s = ""
        else:
            if isinstance(s, str):
                s = datetime.strptime(s, "%Y-%m-%d %H:%M:%S")

            s = datetime.strftime(s, "%d %B %Y")
        return s