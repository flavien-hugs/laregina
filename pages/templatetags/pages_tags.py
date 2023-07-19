import random

from django import template
from pages.models import Annonce
from pages.models import Campaign
from pages.models import Pub
from pages.models import Testimonial

register = template.Library()


@register.inclusion_tag("includes/partials/_partials_video.html")
def publicity_list():
    movies = Pub.objects.filter(is_active=True)
    campaigns = Campaign.objects.published()

    return {"movie": movies, "campaign": campaigns}


@register.inclusion_tag("includes/partials/_partials_annonce.html")
def annonce_list():
    return {"annonce_object_list": Annonce.objects.filter(is_active=True)[:2]}


@register.inclusion_tag("includes/partials/_partials_annonce.html")
def annonce_second_list():
    return {"annonce_object_list": Annonce.objects.filter(is_active=True)[2:4]}


@register.inclusion_tag("includes/partials/_partials_promotion_list.html")
def campaign_list():
    return {
        "campaign_object_list": sorted(
            Campaign.objects.published()[:2], key=lambda x: random.random()
        )
    }


@register.inclusion_tag("includes/partials/_partials_testimonial_list.html")
def testimonial_list(count=5):
    return {"testimonial_object_list": Testimonial.objects.published()[:count]}
