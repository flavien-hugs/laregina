# core/context.py

from core import settings


# HEAD META
def context(request):
    return {
        'title': settings.SITE_NAME,
        'desc': settings.INDEX_DESCRIPTION,
        'description': settings.SITE_DESCRIPTION,
        'keywords': settings.META_KEYWORDS,
        'facebook': 'https://www.facebook.com/laregina.ci/',
        'twitter': 'https://twitter.com/CoteLaregina',
        'request': request
    }