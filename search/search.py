# search.search.py

from django.db.models import Q

from search.models import SearchTerm
from catalogue.models import Product


STRIP_WORDS = [
    'a', 'an', 'and', 'by', 'for', 'from', 'in', 'no', 'not',
    'of', 'on', 'or', 'that', 'the', 'to', 'with'
]


def store(request, q):

    """
        enregistre le texte de la recherche
        note : si le terme de recherche est long d'au moins
        trois caractères, stocker en db
    """
    
    if len(q) > 4:
        term = SearchTerm()
        term.q = q
        term.ip_address = request.META.get('REMOTE_ADDR')
        term.user = None
        if request.user.is_authenticated:
            term.user = request.user
        term.save()


def products(search_text):

    """
        obtenir les produits correspondant au texte de recherche
    """

    words = _prepare_words(search_text)
    products = Product.objects.all()
    results = {}

    for word in words:
        lookups = products.filter(
            Q(name__icontains=word)
            | Q(category__name__icontains=word)
            | Q(user__store__icontains=word)
            | Q(description__icontains=word)
            | Q(slug__icontains=word)
            | Q(price__icontains=word)
        ).distinct()
        
        results['products'] = lookups

    return results

 
def _prepare_words(search_text):

    """
        supprimer les mots courants, limiter à 5 mots
    """

    words = search_text.split()
    for common in STRIP_WORDS:
        if common in words:
            words.remove(common)
    return words[0:5]
