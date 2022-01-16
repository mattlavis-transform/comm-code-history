from datetime import datetime
from classes.database import Database


class Commodity(object):
    def __init__(self, commodity_code):
        self.commodity_code = commodity_code
        self.get_data()
        pass

    def get_data(self):
        self.data = {}
        self.instances = []
        print("getting data")
        sql = """
        select goods_nomenclature_sid, goods_nomenclature_item_id, validity_start_date, validity_end_date 
        from goods_nomenclatures
        where goods_nomenclature_item_id = %s
        and producline_suffix = '80'
        order by validity_start_date desc;
        """
        params = [
            self.commodity_code
        ]
        d = Database()
        rows = d.run_query(sql, params)
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
            
            print(row[0])
        self.data["data"] = self.instances
        
    def to_yyyymmdd(self, s):
        if s is None:
            s = ""
        else:
            s = datetime.strftime(s, "%Y-%m-%d")
        return s
        
    def to_display(self, s):
        if s is None:
            s = ""
        else:
            s = datetime.strftime(s, "%d %B %Y")
        return s