from django.template import Library
from django.template.defaultfilters import stringfilter
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe
import re

register = Library()

@stringfilter
def wsstrip(value, autoescape=None):
    if autoescape:
	esc = conditional_escape
    else:
	esc = lambda x: x
    return mark_safe(re.sub('[\s?!]', '', esc(value)))
wsstrip.needs_autoescape = True
register.filter(wsstrip)