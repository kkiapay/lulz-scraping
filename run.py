from flask import Flask
from flask_cors import CORS
from flask import request
import requests
import urllib.request
from bs4 import BeautifulSoup
from commons import build_response
from commons import utils


app = Flask(__name__)
CORS(app)

@app.route("/api", methods=["GET"])
def search_company():
    if request.args['company_name']:
        return build_response.build_json(utils.execute_request(request.args['company_name']))
    else:
        return "company_name is required"

@app.route("/", methods=["GET"])
def hello_world():
    return "Hello World"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True, threaded=True)
