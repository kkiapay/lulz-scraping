import requests
import json
import requests
import urllib.request
import time
from bs4 import BeautifulSoup
from flask import Flask

app = Flask(__name__)

class URL:
    gufebenin_url = "http://www.gufebenin.org/index.php/entreprises"
    cepici_url = "https://cepici.ci/views/annonces_legales/Affichage_ajax/SearchMany.php"


def call_api(url, type, headers={}, parameters={}, is_json=False):
    """
    Call external API
    :param url:
    :param type:
    :param parameters:
    :param is_json:
    :return:
    """
    app.logger.info("Initiating API Call with following info: url => {} payload => {}".format(url, parameters))
    if "GET" in type:
        response = requests.get(url, headers=headers, params=parameters, timeout=5)
    elif "POST" in type:
        if is_json:
            response = requests.post(url, headers=headers, json=parameters, timeout=5)
        else:
            response = requests.post(url, headers=headers, params=parameters, timeout=5)
    elif "PUT" in type:
        if is_json:
            response = requests.put(url, headers=headers, json=parameters, timeout=5)
        else:
            response = requests.put(url, headers=headers, params=parameters, timeout=5)
    elif "DELETE" in type:
        response = requests.delete(url, headers=headers, params=parameters, timeout=5)
    else:
        raise Exception("unsupported request method.")
    # result = json.loads(response.text)
    result = response.text
    app.logger.info("API response => %s", result)
    return result


def wrap_response_object(dictionnary, url):
    response = dict()
    if url in URL.gufebenin_url:
        response['name'] = dictionnary['name']
        response['instigator'] = dictionnary['Promotteur']
        response['legal_form'] = dictionnary['Forme juridique']
        response['branch_of_activity'] = ''
        response['location'] = dictionnary['location']
        response['rc'] = ''
        response['country'] = 'Benin'
        response['country_code'] = 'BJ'
        response['date'] = ''
    
    return response


def search_on_gufebenin(searched_value):
    """
    Create object python dictionnary base on http://www.gufebenin.org result
    :param url:
    :param searched_value:
    """
    response = call_api(url=URL.gufebenin_url, type="POST", parameters={"filter-search": searched_value})

    soup = BeautifulSoup(response, "html.parser")
    # target form#adminForm
    form_tag = soup.find("form", id="adminForm")

    # extract list of result in that web page
    all_li_tag = form_tag.find_all("li")

    result = []

    for li in all_li_tag:
        if (li.find("span")):
            # get all key {Promotteur; Forme juridique; }
            all_u_tag_content = li.find("span").find_all("u")
        obj = dict()
        # build dict
        obj['name'] = (li.find("h3").contents[2])[2:].strip("\t")
        for u in all_u_tag_content:
            obj[u.contents[0]] = (u.next_sibling)[2:]
            obj['location'] = (u.next_sibling.next_sibling.next_sibling)[15:].strip("\t")
        result.append(wrap_response_object(dictionnary=obj, url=URL.gufebenin_url))
    return result

def search_on_cepici(date=None, rccm=None, company_name=None):
    """
    """
    response = call_api(url=URL.cepici_url, type="GET", parameters={"manydata%5B%5D": "", "manydata%5B%5D": "CI-ABJ-2019-B-8875", "manydata%5B%5D": "IVOIRE EVENTS", "manydata%5B%5D": None, "countInit": 0})

    soup = BeautifulSoup(response, "html.parser")

    # extract all object key
    all_th_tag = soup.find_all('th')
    # extract all key value
    all_td_tag = soup.find_all('td')

    result = []

    for th in all_th_tag:
        obj = dict()
        for td in all_td_tag:
            obj[th.contents[0]] = str(td)
            app.logger.info(td.contents[0])
    result.append(str(soup))
        # result.append(wrap_response_object(dictionnary=obj, url=URL.cepici_url))
    return result