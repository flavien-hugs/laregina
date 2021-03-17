# catalogue filters

from django import template

from pages.models import Promotion, Testimonial

register = template.Library()


@register.inclusion_tag("includes/partials/_partials_promotion_list.html")
def promotion_list(count=8):
    return {
        'promotion_object_list': Promotion.objects.all()[:count]
    }


@register.inclusion_tag("includes/partials/_partials_testimonial_list.html")
def testimonial_list(count=5):
    return {
    	'testimonial_object_list': Testimonial.objects.all()[:count]
    }
