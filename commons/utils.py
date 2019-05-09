import requests
import json
import re as regex
import urllib.request
from bs4 import BeautifulSoup, Comment
from ruamel.yaml import YAML

yaml = YAML(typ='safe')


def call_api(url, type, headers={}, parameters={}, is_json=False):
    """
    Call external API
    :param url:
    :param type:
    :param parameters:
    :param is_json:
    :return:
    """
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
    # app.logger.info("API response => %s", response.url)
    return response



def yaml_to_json():
    yaml_dict = None
    
    with open("parser.yml", "r") as yaml_in, open("parser.json", "w") as json_out:
        yaml_dict = yaml.load(yaml_in)
        json.dump(yaml_dict, json_out)
    
    return yaml_dict



def execute_request(searched_value):
    response_list = get_html_response(query=searched_value)
    result_list = []
    for key in response_list:
        result = extractor(html=response_list[key], endpoint=key)
        if result:
            result_list.append(result)
    return result_list


def get_html_response(parser=yaml_to_json(), query=""):

    response = dict()

    for item in parser['site']:
        for param in parser[item]['parameters']:
            html_response = call_api(url=parser[item]['url'], type=parser[item]['request_type'], parameters={
                param: query
            })
            response[item] = html_response.text

    return response




def extractor(html="", endpoint="", parser=yaml_to_json()):
    """
    :html > represente your html document
    :parser > parser key in .yml file config
    """
    soup = BeautifulSoup(html, "html.parser")

    result = dict()

    other_result = []

    for site in parser[endpoint]['parser']:
        soup_result = []
        if 'selector' in parser[endpoint]['parser'][site]:
            soup_result = soup.select(parser[endpoint]['parser'][site]['selector'])
        else:
            soup_result = soup.select(parser[endpoint]['parser'][site])
        
        for tag_selected in soup_result:
            for element in tag_selected(text=lambda text: isinstance(text, Comment)):
                element.extract()

            if 'selector' in parser[endpoint]['parser'][site]:
                result[site] = regex.search(r"<u>Promotteur</u>:([a-zA-Z ]+)<br>", str(tag_selected)) #parser[endpoint]['parser'][site]['action']
                # other_result = regex.search(r"{}".format(parser[endpoint]['parser'][site]['action']), tag_selected)
            else:
                result[site] = tag_selected.contents[0].strip()

    return result