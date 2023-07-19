import os
from base64 import b64encode

from catalogue.models import Product
from search.models import SearchTerm


def tracking_id(request):
    try:
        return request.session["tracking_id"]
    except KeyError:
        request.session["tracking_id"] = b64encode(os.urandom(36)).decode()
        return request.session["tracking_id"]


def get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR", None)
    return ip


def recommended_from_search(request):
    common_words = frequent_search_words(request)
    from search import search

    matching = []
    for word in common_words:
        results = search.products(word).get("products", [])
        for r in results:
            if r not in matching:
                matching.append(r)
    return matching


def frequent_search_words(request):
    searches = (
        SearchTerm.objects.filter(tracking_id=tracking_id(request))
        .values("q")
        .order_by("-date_search_at")[0:10]
    )

    search_string = "{}".format([search["q"] for search in searches])

    return sort_words_by_frequency(search_string)[0:3]


def sort_words_by_frequency(some_string):
    words = some_string.split()

    ranked_words = [[word, words.count(word)] for word in set(words)]

    sorted_words = sorted(ranked_words, key=lambda word: -word[1])

    return [p[0] for p in sorted_words]


def log_product_view(request, product):
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
            v.ip_address = "127.0.0.1"
        v.user = None
        v.tracking_id = t_id

        if request.user.is_authenticated:
            v.user = request.user
        v.save()


def recommended_from_views(request):
    t_id = tracking_id(request)
    viewed = get_recently_viewed(request)

    from analytics.models import ProductView

    if viewed:
        productviews = ProductView.objects.filter(product__in=viewed).values(t_id)

        t_ids = [v["tracking_id"] for v in productviews]
        if t_ids:
            all_viewed = Product.objects.filter(productview__tracking_id__in=t_ids)
            if all_viewed:
                other_viewed = ProductView.objects.filter(
                    product__in=all_viewed
                ).exclude(product__in=viewed)
                if other_viewed:
                    return Product.objects.filter(
                        productview__in=other_viewed
                    ).distinct()[:10]


def get_recently_viewed(request):
    from analytics.models import ProductView

    t_id = tracking_id(request)
    views = (
        ProductView.objects.filter(tracking_id=t_id)
        .values("product_id")
        .order_by("-date_viewed")
    )

    product_ids = [v["product_id"] for v in views]
    return Product.objects.filter(id__in=product_ids)[:10]
