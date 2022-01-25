import os
from datetime import datetime
from flask import Flask, request, jsonify
from classes.sqlite_helper import DatabaseLite


class Application(object):
    def __init__(self):
        pass
    
    def get_measure_types(self):
        data = {}
        instances = []
        snapshot_date = request.args.get('as_of')

        database_filename = os.path.join(os.getcwd(), "db", "commodity-code-history.db")
        db = DatabaseLite(database_filename)

        if snapshot_date:
            sql = """
            select measure_type_id, measure_type_description, measure_type_series_id,
            measure_type_series_description, trade_movement_code, measure_component_applicable_code,
            order_number_capture_code, validity_start_date, validity_end_date
            from measure_types mt
            where validity_start_date <= """ + snapshot_date + """
            and validity_end_date >= """ + snapshot_date + """ or validity_end_date is null
            order by 1;
            """
        else:
            sql = """
            select measure_type_id, measure_type_description, measure_type_series_id,
            measure_type_series_description, trade_movement_code, measure_component_applicable_code,
            order_number_capture_code, validity_start_date, validity_end_date
            from measure_types mt order by 1;
            """
            
        rows = db.run_query(sql)
        for row in rows:
            instance = {
                "measure_type_id": row[0],
                "measure_type_description": row[1],
                "measure_type_series_id": row[2],
                "measure_type_series_description": row[3],
                "trade_movement_code": row[4],
                "measure_component_applicable_code": row[5],
                "order_number_capture_code": row[6],
                "validity_start_date": self.to_yyyymmdd(row[7]),
                "validity_end_date": self.to_yyyymmdd(row[8])
            }
            instances.append(instance)
        
        data["data"] = instances

        return data

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
