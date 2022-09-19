import os
from django import template

register = template.Library()

@register.filter
def to_and(value):
    return value.replace("repositorio_archivos/"+os.sep," ", 3).replace("repositorio_archivos/","", 3).replace("\\"," ", 100)