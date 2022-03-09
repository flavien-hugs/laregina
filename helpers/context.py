# core/context.py

from core import settings


# HEAD META
def context(request):
    return {
        'title': settings.SITE_NAME,
        'desc': settings.INDEX_DESCRIPTION,
        'description': settings.SITE_DESCRIPTION,
        'keywords': settings.META_KEYWORDS,
        'address': "Ahougnansou, Bouaké - Côte d'Ivoire",
        'contact_one': '+225 07 7872 2639',
        'contact_two': '07 4747 3627',
        'contact_three': '07 7872 2639',
        'email_info': 'infos@laregina.deals',
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


# CSRF_FAILURE_VIEW
def csrf_failure(request, reason=""):
    ctx = {
        'message': 'Oops veuillez actualiser votre page, votre session est expirée.'
    }
    template = 'includes/partials/403_csrf.html'
    return render_to_reponse(request, template, ctx)