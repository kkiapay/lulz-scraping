from flask import Flask
from flask import request
import requests
import urllib.request
import time
from bs4 import BeautifulSoup
from commons import build_response
from commons import utils


app = Flask(__name__)

@app.route("/api", methods=["POST"])
def search_company():
    if request.form['company_name']:
        result = utils.search_on_gufebenin(searched_value=request.form['company_name'])
        result_ci = utils.search_on_cepici(company_name=request.form['company_name'], rccm=request.form['rccm'])
        return build_response.build_json(result + result_ci)
    else:
        return "company_name is required"

@app.route("/", methods=["GET"])
def hello_world():
    return "Hello World"

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True, threaded=True)
