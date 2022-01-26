import os
from datetime import datetime
from flask import Flask, request, jsonify
from markupsafe import re
from classes.sqlite_helper import DatabaseLite


class Application(object):
    def __init__(self):
        self.database_filename = os.path.join(os.getcwd(), "db", "commodity-code-history.db")

    def get_commodity_history(self):
        data = {}
        instances = []
        commodity_code = request.args.get('c')

        db = DatabaseLite(self.database_filename)

        sql = """select goods_nomenclature_sid, goods_nomenclature_item_id, validity_start_date, validity_end_date 
        from goods_nomenclatures
        where goods_nomenclature_item_id = '""" + commodity_code + """'
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
            instances.append(instance)
        data["data"] = instances

        return data

    def get_document_codes(self):
        data = {}
        instances = []
        code = request.args.get('c')

        db = DatabaseLite(self.database_filename)

        if code is None:
            sql = """
            select code, certificate_type_code, certificate_code, validity_start_date,
            certificate_description, certificate_type_description
            from document_codes dc order by code;
            """
        else:
            sql = """
            select code, certificate_type_code, certificate_code, validity_start_date,
            certificate_description, certificate_type_description
            from document_codes dc where code = '""" + code + """' order by code 
            """
            
        rows = db.run_query(sql)
        for row in rows:
            instance = {}
            attributes = {}
            
            attributes["certificate_type_code"] = row[1]
            attributes["certificate_code"] = row[2]
            attributes["validity_start_date"] = row[3]
            attributes["certificate_description"] = row[4]
            attributes["certificate_type_description"] = row[5]
            
            instance["id"] = row[0]
            instance["type"] = "document_code"
            instance["attributes"] = attributes
            
            instances.append(instance)
            data["data"] = instances

        return data

    def get_quotas(self):
        from_date = request.args.get('from')
        to_date = request.args.get('to')

        instances = []
        data = {}
        db = DatabaseLite(self.database_filename)
        if from_date and to_date:
            sql = """
            select * from quota_order_numbers
            where definition_start_date <= '""" + to_date + """'
            and definition_end_date >= '""" + from_date + """'
            order by quota_order_number_id, quota_start_date, definition_start_date
            """
        else:
            sql = """
            select * from quota_order_numbers
            order by quota_order_number_id, quota_start_date, definition_start_date
            """
        
        rows = db.run_query(sql)
        previous_order_number = -1
        for row in rows:
            if previous_order_number != row[1]:
                if previous_order_number != -1:
                    instances.append(instance)

                instance = {}
                attributes = {}
                relationships = []
                
                attributes["sid"] = row[0]
                attributes["quota_start_date"] = self.to_yyyymmdd(row[2])
                attributes["quota_end_date"] = self.to_yyyymmdd(row[3])
                
                relationship = self.get_relationship(row)
                relationships.append(relationship)
                
                instance["id"] = row[1]
                instance["type"] = "quota_order_number"
                instance["attributes"] = attributes
                instance["relationships"] = relationships
            else:
                relationship = self.get_relationship(row)
                relationships.append(relationship)
            
            previous_order_number = row[1]

        if instance:
            instances.append(instance)
            
        data["data"] = instances

        return data
    
    def get_relationship(self, row):
        relationship = {}
        attributes = {}
        relationship["id"] = row[4]
        relationship["type"] = "quota_definition"
        attributes["id"] = row[4]
        attributes["validity_start_date"] = self.to_yyyymmdd(row[5])
        attributes["validity_end_date"] = self.to_yyyymmdd(row[6])
        attributes["initial_volume"] = row[7]
        attributes["measurement_unit_code"] = row[8]
        attributes["measurement_unit_qualifier_code"] = row[9]
        attributes["maximum_precision"] = row[10]
        attributes["critical_state"] = row[11]
        attributes["critical_threshold"] = row[12]
        relationship["attributes"] = attributes
        return relationship

    def get_measure_types(self):
        data = {}
        instances = []
        snapshot_date = request.args.get('as_of')
        db = DatabaseLite(self.database_filename)
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
            instance = {}
            attributes = {}
            
            attributes["description"] = row[1]
            attributes["measure_type_series_id"] = row[2]
            attributes["measure_type_series_description"] = row[3]
            attributes["trade_movement_code"] = row[4]
            attributes["measure_component_applicable_code"] = row[5]
            attributes["order_number_capture_code"] = row[6]
            attributes["validity_start_date"] = self.to_yyyymmdd(row[7])
            attributes["validity_end_date"] = self.to_yyyymmdd(row[8])
            
            instance["id"] = row[0]
            instance["type"] = "measure_type"
            instance["attributes"] = attributes
            
            instances.append(instance)
        
        data["data"] = instances

        return data


    def get_condition_codes(self):
        data = {}
        instances = []
        db = DatabaseLite(self.database_filename)
        sql = """
        select * from measure_condition_codes order by 1;
        """
            
        rows = db.run_query(sql)
        for row in rows:
            instance = {}
            attributes = {}
            
            attributes["id"] = row[0]
            attributes["validity_start_date"] = self.to_yyyymmdd(row[1])
            attributes["validity_end_date"] = self.to_yyyymmdd(row[2])
            attributes["description"] = row[3]

            instance["id"] = row[0]
            instance["type"] = "measure_condition_code"
            instance["attributes"] = attributes
            
            instances.append(instance)
        
        data["data"] = instances

        return data


    def get_action_codes(self):
        data = {}
        instances = []
        db = DatabaseLite(self.database_filename)
        sql = """
        select * from measure_actions order by 1;
        """
            
        rows = db.run_query(sql)
        for row in rows:
            instance = {}
            attributes = {}
            
            attributes["id"] = row[0]
            attributes["validity_start_date"] = self.to_yyyymmdd(row[1])
            attributes["validity_end_date"] = self.to_yyyymmdd(row[2])
            attributes["description"] = row[3]

            instance["id"] = row[0]
            instance["type"] = "measure_action"
            instance["attributes"] = attributes
            
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
