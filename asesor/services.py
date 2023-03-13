from typing import Any, Dict
import requests
import simplejson

from builtins import print
import delorean
from django.http import JsonResponse
from django.shortcuts import render, redirect
from eva.models import Ciclo, Ciclo2
from .models import CoursesMoodle
import requests
from datetime import datetime, date, timedelta, time
from conf.models import Carrera, Facultad
from django.core import serializers
from conf.models import Carrera
from authentication.models import Usuario, FacultyUser,RolUser
from django.core.serializers import json
from django.core import serializers
# Create your views here.
from django.views import View
from django.http import HttpResponse
from auditoria.apps import GeneradorAuditoria

from secoed.settings import TOKEN_MOODLE, API_BASE
import requests



def generate_request(url:str, params:Dict, verb:str = "GET")-> Any:
    response = requests.get(url, params) if verb == "GET" else requests.post(url, params)
    
    if (
            response.status_code != 204 and
            response.headers["content-type"].strip().startswith("application/json")
        ):
            try:
                return response.json()
            except ValueError:
                 raise SyntaxError("no marker found")
    

def obtener_datos(params:Dict,verb:str = "GET")-> Any:
    defaultParams:Dict = {
        "wstoken": "f3daa936736c02613b285fe50f4616a5",
        "moodlewsrestformat": "json"
    }
    defaultParams.update(params)
    response:Any=generate_request("https://secoed.com/aula-virtual/webservice/rest/server.php",defaultParams, verb)
    return response