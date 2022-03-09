# catalogue filters

from django import template

from pages.models import(
    Campaign, Pub, Annonce, Testimonial
)

register = template.Library()


@register.inclusion_tag("includes/partials/_partials_video.html")
def publicity_list(count=2):
    return {
    	'video_object_list': Pub.objects.filter(is_active=True)[:count]
    }


@register.inclusion_tag("includes/partials/_partials_annonce.html")
def annonce_list():
    return {
    	'annonce_object_list': Annonce.objects.filter(is_active=True)[:2]
    }

@register.inclusion_tag("includes/partials/_partials_annonce.html")
def annonce_second_list():
    return {
        'annonce_object_list': Annonce.objects.filter(is_active=True)[2:4]
    }

@register.inclusion_tag("includes/partials/_partials_promotion_list.html")
def promotion_list(count=8):
    return {
        'promotion_object_list': Campaign.objects.published()[:count]
    }


@register.inclusion_tag("includes/partials/_partials_testimonial_list.html")
def testimonial_list(count=5):
    return {
    	'testimonial_object_list': Testimonial.objects.published()[:count]
    }
