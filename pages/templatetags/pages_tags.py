# catalogue filters

from django import template

from pages import models

register = template.Library()


@register.inclusion_tag("includes/partials/_partials_promotion_list.html")
def promotion_list(count=8):
    return {
        'promotion_object_list': models.Promotion.objects.filter(active=True)[:count]
    }


@register.inclusion_tag("includes/partials/_partials_testimonial_list.html")
def testimonial_list(count=5):
    return {
    	'testimonial_object_list': models.Testimonial.objects.filter(activate_at=True)[:count]
    }
