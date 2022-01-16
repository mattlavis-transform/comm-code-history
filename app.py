# app.py
from flask import Flask, request, jsonify
import os
from classes.commodity import Commodity
from classes.sqlite_helper import DatabaseLite


app = Flask(__name__)

# A welcome message to test our server
@app.route('/')
def index():
    return "<h1>Welcome to our server !!</h1>"

@app.route('/commodity', methods=['GET'])
def get_commodity():
    commodity_code = request.args.get('c')
    c = Commodity(commodity_code)
    return c.data
    # return "<h1>Getting a commodity " + commodity_code + " </p>"

# Test SQLLite3
@app.route('/sqlite3')
def sqlite3():
    database_filename = os.path.join(os.getcwd(), "db", "commodity-code-history.db")
    db = DatabaseLite(database_filename)
    sql = "select * from goods_nomenclatures limit 10;"
    rows = db.run_query(sql)

    return "<h1>SQLite</h1>"



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
