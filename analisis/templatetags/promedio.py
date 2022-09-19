import os
from django import template

register = template.Library()

@register.simple_tag(name='promedio')
def promedio(a,b):
    return str(sum(a)/len(b))