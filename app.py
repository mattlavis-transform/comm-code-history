# app.py
from flask import Flask, request, jsonify
import os
from classes.commodity import Commodity
from classes.commodity2 import Commodity2
from classes.sqlite_helper import DatabaseLite


app = Flask(__name__)

# A welcome message to test our server
@app.route('/')
def index():
    return "<h1>Welcome to our server !!</h1>"

@app.route('/commodities', methods=['GET'])
def get_commodity():
    commodity_code = request.args.get('c')
    c = Commodity(commodity_code)
    return c.data

@app.route('/commodities2', methods=['GET'])
def get_commodity2():
    # commodity_code = request.args.get('c')
    c = Commodity2()
    return c.data

@app.route('/sqlite3')
def sqlite3():
    database_filename = os.path.join(os.getcwd(), "db", "commodity-code-history.db")
    db = DatabaseLite(database_filename)
    sql = "select * from goods_nomenclatures limit 10;"
    rows = db.run_query(sql)

    return "<h1>SQLite</h1>"

@app.route('/sqlite4')
def sqlite4():
    database_filename = os.path.join(os.getcwd(), "db", "commodity-code-history.db")
    db = DatabaseLite(database_filename)
    sql = "select * from goods_nomenclatures limit 10;"
    
    commodity_code = "0101291000"
    sql = """select goods_nomenclature_sid, goods_nomenclature_item_id, validity_start_date, validity_end_date 
    from goods_nomenclatures
    where goods_nomenclature_item_id = '""" + commodity_code + """'
    order by validity_start_date desc;
    """
        
    rows = db.run_query(sql)
    row = rows[0]
    instance = {
        "sid": 123,
        "goods_nomenclature_item_id": row[0],
        "validity_start_date": "test",
        "validity_end_date": "test",
        "validity_start_date_display": "test",
        "validity_end_date_display": "test"
    }
    data = {}
    data["data"] = instance

    return data

# Test SQLLite3
@app.route('/flaps')
def flaps():
    return "<h1>Flaps</h1>"



@app.route('/getmsg/', methods=['GET'])
def respond():
    # Retrieve the name from url parameter
    name = request.args.get("name", None)

    # For debugging
    print(f"got name {name}")

    response = {}

    # Check if user sent a name at all
    if not name:
        response["ERROR"] = "no name found, please send a name."
    # Check if the user entered a number not a name
    elif str(name).isdigit():
        response["ERROR"] = "name can't be numeric."
    # Now the user entered a valid name
    else:
        response["MESSAGE"] = f"Welcome {name} to our awesome platform!!"

    # Return the response in json format
    return jsonify(response)

@app.route('/post/', methods=['POST'])
def post_something():
    param = request.form.get('name')
    print(param)
    # You can add the test cases you made in the previous function, but in our case here you are just testing the POST functionality
    if param:
        return jsonify({
            "Message": f"Welcome {name} to our awesome platform!!",
            # Add this option to distinct the POST request
            "METHOD" : "POST"
        })
    else:
        return jsonify({
            "ERROR": "no name found, please send a name."
        })

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)
