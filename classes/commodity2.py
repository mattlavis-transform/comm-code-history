from datetime import datetime
from classes.database import Database
from classes.sqlite_helper import DatabaseLite
import os


class Commodity2(object):
    def __init__(self):
        self.commodity_code = "0702000007"
        a = 1
        self.get_date_sql_lite()
        pass
    
    def get_date_sql_lite(self):
        self.data = {}
        self.instances = []
        database_filename = os.path.join(os.getcwd(), "db", "commodity-code-history.db")
        db = DatabaseLite(database_filename)
        sql = """select goods_nomenclature_sid, goods_nomenclature_item_id, validity_start_date, validity_end_date 
        from goods_nomenclatures
        where goods_nomenclature_item_id = '""" + self.commodity_code + """'
        order by validity_start_date desc;
        """
        rows = db.run_query(sql)
        for row in rows:
            instance = {
                "sid": row[0],
                "goods_nomenclature_item_id": row[1],
                "validity_start_date": self.to_yyyymmdd(row[2]),
                "validity_end_date": self.to_yyyymmdd(row[3]),
                "validity_start_date_display": self.to_display(row[2]),
                "validity_end_date_display": self.to_display(row[3])
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
