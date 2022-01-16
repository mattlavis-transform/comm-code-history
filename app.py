import flask
from flask import request
from classes.commodity import Commodity

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def home():
    return "<h1>Distant Reading Archive</h1><p>This site is a prototype API for distant reading of science fiction novels.</p>"


@app.route('/commodity', methods=['GET'])
def get_commodity():
    commodity_code = request.args.get('c')
    c = Commodity(commodity_code)
    return c.data
    # return "<h1>Getting a commodity " + commodity_code + " </p>"

app.run()
