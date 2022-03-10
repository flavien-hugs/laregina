# analytics/utils.py

import os
from base64 import b64encode
from django.shortcuts import get_object_or_404

from search.models import SearchTerm
from catalogue.models import Product


def tracking_id(request):
    """ unique ID to determine what pages a customer has viewed """
    try:
        return request.session['tracking_id']
    except KeyError:
        request.session['tracking_id'] = b64encode(os.urandom(36)).decode()
        return request.session['tracking_id']


def get_client_ip(request):

    '''
    capturer l'adresse ip
    '''
    
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR', None)
    return ip


def recommended_from_search(request):

    """
        obtenir les mots communs à partir des recherches stockées
    """

    common_words = frequent_search_words(request)
    from search import search
    matching = []
    for word in common_words:
        results = search.products(word).get('products', [])
        for r in results:
            if not r in matching:
                matching.append(r)
    return matching


def frequent_search_words(request):

    """ 
        obtient les trois mots de recherche les plus courants
        parmi les 10 dernières recherches effectuées
        par le client actuel
    """

    # obtenir les dix recherches les plus récentes dans la base de données.
    searches = SearchTerm.objects.filter(
        tracking_id=tracking_id(request)
        ).values('q').order_by('-date_search_at')[0:10]

    # regrouper toutes les recherches en une seule chaîne.
    search_string = '{}'.format([search['q'] for search in searches])

    # retourner les trois mots les plus courants dans les recherches
    return sort_words_by_frequency(search_string)[0:3]


def sort_words_by_frequency(some_string):
    """
        prend une seule chaîne de mots délimitée par des espaces
        et renvoie une liste de mots qu'ils contiennent,
        du plus fréquent au moins fréquent
    """

    # convertir la chaîne de caractères en une liste python
    words = some_string.split()
    
    # attribuer un rang à chaque mot en fonction de sa fréquence
    ranked_words = [[word, words.count(word)] for word in set(words)]
    
    # trier les mots en fonction de leur fréquence décroissante
    sorted_words = sorted(ranked_words, key=lambda word: -word[1])
    
    # log the current customer as having viewed the given product instance
    return [p[0] for p in sorted_words]


def log_product_view(request, product):
    
    """
    enregistrer le client actuel comme ayant
    consulté l'instance du produit donné
    """
    
    t_id = tracking_id(request)
    from analytics.models import ProductView
    try:
        v = ProductView.objects.get(tracking_id=t_id, product=product)
        v.save()
    except ProductView.DoesNotExist:
        v = ProductView()
        v.product = product
        v.ip_address = get_client_ip(request)
        
        if not get_client_ip(request):
            v.ip_address = '127.0.0.1'
        v.user = None
        v.tracking_id = t_id
        
        if request.user.is_authenticated:
            v.user = request.user
        v.save()


def recommended_from_views(request):
    
    """
        obtenir des recommandations de produits basées sur
        les produits que le client a consultés; obtenir la
        liste des identifiants de suivi des autres clients
        qui ont consulté les produits dans les produits
        consultés par le client actuel, et obtenir les
        produits que ces autres clients ont également consultés.
    """

    t_id = tracking_id(request)
    
    # obtenir les produits récemment consultés
    viewed = get_recently_viewed(request)
    
    # si des produits ont déjà été consultés, obtenir
    # d'autres adresse ip de suivi qui ont également
    # consulté ces produits

    from analytics.models import ProductView
    if viewed:
        productviews = ProductView.objects.filter(
            product__in=viewed).values('tracking_id')
        
        t_ids = [v['tracking_id'] for v in productviews]
        
        # s'il existe d'autres identifiants de suivi,
        # obtenir les produits que ces autres clients
        # ont consultés.
        if t_ids:
            all_viewed = Product.objects.filter(productview__tracking_id__in=t_ids)
            # s'il existe d'autres produits, les obtenir,
            # à l'exclusion des produits que le client a déjà consultés.
            if all_viewed:
                other_viewed = ProductView.objects.filter(
                    product__in=all_viewed).exclude(product__in=viewed)
                if other_viewed:
                    return Product.objects.filter(
                        productview__in=other_viewed).distinct()[:10]


def get_recently_viewed(request):
    from analytics.models import ProductView
    t_id = tracking_id(request)
    views = ProductView.objects.filter(
        tracking_id=t_id).values('product_id').order_by('-date_viewed')
    
    product_ids = [v['product_id'] for v in views]
    return Product.objects.filter(id__in=product_ids)[:10]
