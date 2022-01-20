# app.py
from flask import Flask, request, jsonify
import os
from datetime import datetime
from collections import OrderedDict
from classes.commodity import Commodity
from classes.commodity2 import Commodity2
from classes.sqlite_helper import DatabaseLite


app = Flask(__name__)

def to_yyyymmdd(s):
    if s is None:
        s = ""
    else:
        if isinstance(s, str):
            s = datetime.strptime(s, "%Y-%m-%d %H:%M:%S")
        
        s = datetime.strftime(s, "%Y-%m-%d")
    return s
    
def to_display(s):
    if s is None:
        s = ""
    else:
        if isinstance(s, str):
            s = datetime.strptime(s, "%Y-%m-%d %H:%M:%S")

        s = datetime.strftime(s, "%d %B %Y")
    return s


# A welcome message to test our server
@app.route('/')
def index():
    return "<h1>Welcome to our server !!</h1>"

@app.route('/xcommodities', methods=['GET'])
def get_commodity():
    commodity_code = request.args.get('c')
    c = Commodity(commodity_code)
    return c.data

@app.route('/sqlite3')
def sqlite3():
    database_filename = os.path.join(os.getcwd(), "db", "commodity-code-history.db")
    db = DatabaseLite(database_filename)
    sql = "select * from goods_nomenclatures limit 10;"
    rows = db.run_query(sql)

    return "<h1>SQLite</h1>"

@app.route('/commodities')
def commodities_local():
    data = {}
    instances = []
    commodity_code = request.args.get('c')

    database_filename = os.path.join(os.getcwd(), "db", "commodity-code-history.db")
    db = DatabaseLite(database_filename)

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
            "validity_start_date": to_yyyymmdd(row[2]),
            "validity_end_date": to_yyyymmdd(row[3]),
            "validity_start_date_display": to_display(row[2]),
            "validity_end_date_display": to_display(row[3])
        }
        instances.append(instance)
    data["data"] = instances

    return data

@app.route('/document-codes')
def document_codes_local():
    # data = {}
    data = OrderedDict()
    instances = []
    code = request.args.get('c')

    database_filename = os.path.join(os.getcwd(), "db", "commodity-code-history.db")
    db = DatabaseLite(database_filename)

    if code is None:
        sql = """
        select code, description, certificate_type_code, certificate_code, validity_start_date
        from certificates c order by code;
        """
    else:
        sql = """
        select code, description, certificate_type_code, certificate_code, validity_start_date
        from certificates c where code = '""" + code + """' order by code 
        """
        
    rows = db.run_query(sql)
    for row in rows:
        instance = OrderedDict()
        attributes = OrderedDict()
        
        attributes["certificate_type_code"] = row[2]
        attributes["certificate_code"] = row[3]
        attributes["description"] = row[1]
        attributes["validity_start_date"] = row[4]
        
        instance["id"] = row[0]
        instance["type"] = "certificates"
        instance["attributes"] = attributes
        
        # instance = {
        #     "id": row[0],
        #     "type": "certificates",
        #     "attributes": {
        #         "certificate_type_code": row[2],
        #         "certificate_code": row[3],
        #         "description": row[1],
        #         "validity_start_date": to_display(row[4])
        #     }
        # }
        instances.append(instance)
    data["data"] = instances

    return data

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)
