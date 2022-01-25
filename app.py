# app.py
from flask import Flask, request


import globals as g

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False


@app.route('/')
def index():
    return "<h1>Welcome to our server !!</h1>"


@app.route('/commodities')
def get_commodity_history():
    commodity_history = g.app.get_commodity_history()
    return commodity_history


@app.route('/measure-types')
def get_measure_types():
    measure_types = g.app.get_measure_types()
    return measure_types


@app.route('/document-codes')
def get_document_codes():
    document_codes = g.app.get_document_codes()
    return document_codes


@app.route('/quotas')
def get_quotas():
    quotas = g.app.get_quotas()
    return quotas


if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)
