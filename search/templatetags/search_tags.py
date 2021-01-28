# search.templatetags.search_tags.py

import urllib
from django import template

from search.forms import SearchForm

register = template.Library()


@register.inclusion_tag("search/search_box.html")
def search_box(request):
    q = request.GET.get('q', None)
    return {'form': SearchForm({'q': q})}
