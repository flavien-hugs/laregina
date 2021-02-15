# catalogue filters

import locale
from django import template

from pages.models import Promotion

register = template.Library()


@register.inclusion_tag("includes/partials/_partials_promotion_list.html")
def promotion_list(count=8):
    return {
        'object_list': Promotion.objects.all()[:count],
    }
