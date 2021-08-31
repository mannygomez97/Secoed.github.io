from typing import Any, Dict
import requests

def generate_request(url:str, params:Dict, verb:str = "GET")-> Any:
    response = requests.get(url, params) if verb == "GET" else requests.post(url, params)
    return response.json()

def obtener_datos(params:Dict,verb:str = "GET")-> Any:
    defaultParams:Dict = {
        "wstoken": "958c77e27c859fac94cfb40ceec68a06",
        "moodlewsrestformat": "json"
    }
    defaultParams.update(params)
    response:Any=generate_request("http://academyec.com/moodle/webservice/rest/server.php",defaultParams, verb)
    return response