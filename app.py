# app.py
from flask import Flask, request
from flask_cors import CORS


import globals as g

app = Flask(__name__)
CORS(app)
app.config['JSON_SORT_KEYS'] = False


@app.route('/')
def index():
    return "<h1>Welcome to our server !!</h1>"


@app.route('/commodities')
def get_commodity_history():
    commodity_history = g.app.get_commodity_history()
    return commodity_history


@app.route('/guidance')
def get_guidance():
    guidance = g.app.get_guidance()
    return guidance


@app.route('/measure-types')
def get_measure_types():
    measure_types = g.app.get_measure_types()
    return measure_types


@app.route('/document-codes')
def get_document_codes():
    document_codes = g.app.get_document_codes()
    return document_codes


@app.route('/certificate_codes')
def get_certificate_codes():
    document_codes = g.app.get_document_codes()
    return document_codes


@app.route('/quotas')
def get_quotas():
    quotas = g.app.get_quotas()
    return quotas


@app.route('/condition-codes')
def get_condition_codes():
    condition_codes = g.app.get_condition_codes()
    return condition_codes


@app.route('/action-codes')
def get_action_codes():
    action_codes = g.app.get_action_codes()
    return action_codes


@app.route('/commodities/<goods_nomenclature_item_id>')
def get_commodity(goods_nomenclature_item_id):
    # return "The product is " + str(goods_nomenclature_item_id)
    commodity = g.app.get_commodity(goods_nomenclature_item_id)
    return commodity


@app.route('/quotas/<quota_order_number_id>')
def get_quota(quota_order_number_id):
    # return "The order number is " + str(quota_order_number_id)
    quota = g.app.get_quota(quota_order_number_id)
    a = 1
    return quota


@app.route('/quota_definition/<quota_definition_sid>')
def get_quota_definition(quota_definition_sid):
    quota_definition = g.app.get_quota_definition(quota_definition_sid)
    return quota_definition


@app.route('/quota_measures/<quota_order_number_id>')
def get_quota_measures(quota_order_number_id):
    # return "The order number is " + str(quota_order_number_id)
    quota = g.app.get_quota_measures(quota_order_number_id)
    a = 1
    return quota


if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    # app.run(threaded=True, port=5000, debug=True)
    app.run(threaded=True, port=5000)
