# core/context.py

from core import settings


# HEAD META
def context(request):
    return {
        'title': settings.SITE_NAME,
        'desc': settings.INDEX_DESCRIPTION,
        'description': settings.SITE_DESCRIPTION,
        'keywords': settings.META_KEYWORDS,
        'contact_one': '30 63 04 19',
        'contact_two': '47 47 36 27',
        'email_info': 'infos@laregina-ci.com',
        'facebook': 'https://www.facebook.com/laregina.ci/',
        'twitter': 'https://twitter.com/CoteLaregina',
        'request': request
    }

# category
def category(request):
    from category.models import Category
    return {'category': Category.objects.all()}

# shopcart
def cart_items(request):
    from cart.cart import get_cart_items
    return {
        'cart_items': get_cart_items(request)
    }
