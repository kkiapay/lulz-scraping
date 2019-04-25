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
        response = requests.get(url, headers=headers, params=parameters)
    elif "POST" in type:
        if is_json:
            response = requests.post(url, headers=headers, json=parameters)
        else:
            response = requests.post(url, headers=headers, params=parameters)
    elif "PUT" in type:
        if is_json:
            response = requests.put(url, headers=headers, json=parameters)
        else:
            response = requests.put(url, headers=headers, params=parameters)
    elif "DELETE" in type:
        response = requests.delete(url, headers=headers, params=parameters)
    else:
        raise Exception("unsupported request method.")
    # result = json.loads(response.text)
    app.logger.info("API response => %s", response.url)
    return response


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
        response['country_code'] = '229'
        response['code_iso'] = 'BJ'
        response['date'] = ''
        response['other_information'] = ''
    elif url in URL.cepici_url:
        response['name'] = dictionnary['Raison Sociale']
        response['instigator'] = ''
        response['legal_form'] = dictionnary['Statut Juridique']
        response['branch_of_activity'] = ''
        response['location'] = ''
        response['rc'] = dictionnary['N° RCCM']
        response['country'] = "Côte d'Ivoire"
        response['county_code'] = '225'
        response['code_iso'] = 'CI'
        response['date'] = dictionnary['Date']
        response['other_information'] = dictionnary['more']
    
    return response


def search_on_gufebenin(searched_value):
    """
    Create object python dictionnary base on http://www.gufebenin.org result
    :param url:
    :param searched_value:
    """
    response = call_api(url=URL.gufebenin_url, type="POST", parameters={"filter-search": searched_value})

    soup = BeautifulSoup(response.text, "html.parser")
    # target form#adminForm
    form_tag = soup.find('form', id='adminForm')

    # extract list of result in that web page
    all_li_tag = form_tag.find_all("li")

    result = []

    for li in all_li_tag:
        if (li.find('span')):
            # get all key {Promotteur; Forme juridique; }
            all_u_tag_content = li.find('span').find_all('u')
        obj = dict()
        # build dict
        obj['name'] = (li.find("h3").contents[2])[2:].strip("\t")
        for u in all_u_tag_content:
            obj[u.contents[0]] = (u.next_sibling)[2:]
            obj['location'] = (u.next_sibling.next_sibling.next_sibling)[15:].strip("\t")
        result.append(wrap_response_object(dictionnary=obj, url=URL.gufebenin_url))
    return result

def search_on_cepici(date="", rccm="", company_name=""):
    """
    """
    response = call_api(url=URL.cepici_url+'?'+"manydata[]="+date+"&"+"manydata[]="+rccm+"&"+"manydata[]="+company_name+"&"+"manydata[]=&"+"countInit=0", type="GET")

    soup = BeautifulSoup(response.text, "html.parser")

    # extract all object key
    all_th_tag = soup.find('thead').find('tr').find_all('th')
    key_content = []
    for key in all_th_tag:
        key_content.append(key.contents[0])
    
    # extract all value of each key
    all_tr_result = soup.find_all('tr', id='contenu')

    result = []

    for tr in all_tr_result:
        obj = dict()
        for key, value in zip(key_content, tr.find_all('td')):
            if (key in "Raison Sociale"):
                obj[key] = value.contents[1].contents[0].strip()
                obj['more'] = value.contents[1].get('href')
            else:
                obj[key] = value.contents[0]
        result.append(wrap_response_object(dictionnary=obj, url=URL.cepici_url))
    return result