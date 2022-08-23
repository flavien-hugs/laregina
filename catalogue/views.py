# catalogue.views.py

import random
from django.db.models import Q
from django.conf import settings
from django.views import generic
from django.utils import timezone
from django.contrib import messages
from django.core.cache import cache
from django.utils.safestring import mark_safe
from django.contrib.auth import get_user_model
from django.urls import reverse, reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404

from cart import cart
from analytics import utils
from category.models import Category

from catalogue.models import Product
from pages.mixins import PromotionMixin
from reviews.models import ProductReview
from catalogue.filters import FilterMixin
from reviews.forms import ProductReviewForm
from pages.models import Promotion, HomePage
from catalogue.forms import ProductAddToCartForm


class ExtraContextData:

    queryset = Category.objects.all()

    def get_context_data(self, **kwargs):
        kwargs['promotions'] = self.promotions()
        kwargs['destockages'] = self.get_destockages()
        kwargs['sales_flash'] = self.get_sales_flash()
        kwargs['news_arrivals'] = self.get_news_arrivals()

        kwargs['promotion_list'] = self.get_promotions_list()[:6]
        kwargs['vendor_list'] = get_list_or_404(get_user_model())[0:8]
        kwargs['recently_viewed'] = utils.get_recently_viewed(
            request=self.request)
        kwargs['category_list'] = self.queryset.get_ancestors(
            include_self=False)

        supermarket = self.queryset.get(
            pk=7).get_descendants(include_self=True)
        kwargs['supermarkets'] = Product.objects.filter(
            category__in=supermarket)[:15]

        supermarkets = self.queryset.get(
            pk=22).get_descendants(include_self=True)
        kwargs['categories'] = supermarkets.get_ancestors(include_self=False)
        kwargs['products'] = Product.objects.filter(
            category__in=supermarkets)[:15]

        return super().get_context_data(**kwargs)


class HomeView(ExtraContextData, PromotionMixin, generic.TemplateView):

    template_name = "index.html"

    def dispatch(self, request, *args, **kwargs):
        if HomePage.objects.filter(page=1):
            return HttpResponseRedirect(reverse_lazy("market"))
        elif HomePage.objects.filter(page=2):
            return HttpResponseRedirect(reverse_lazy("allmarket"))
        return super().dispatch(request, *args, **kwargs)


home_view = HomeView.as_view()


class HomeMarketView(ExtraContextData, PromotionMixin, generic.TemplateView):

    template_name = "market.html"

    def get_context_data(self, **kwargs):

        sococe = self.queryset.get(pk=24).get_descendants(include_self=True)
        bonprix = self.queryset.get(pk=26).get_descendants(include_self=True)
        greatmarket = self.queryset.get(pk=23).get_descendants(include_self=True)
        sococe_details = self.queryset.get(pk=25).get_descendants(include_self=True)

        kwargs['sococes'] = Product.objects.filter(category__in=sococe)[:15]
        kwargs['bestprices'] = Product.objects.filter(category__in=bonprix)[:15]
        kwargs['greatmarket'] = Product.objects.filter(category__in=greatmarket)[:15]
        kwargs['sococedetails'] = Product.objects.filter(category__in=sococe_details)[:15]

        return super().get_context_data(**kwargs)


home_market_view = HomeMarketView.as_view()


class HomeTwoView(ExtraContextData, PromotionMixin, generic.TemplateView):

    template_name = 'market.html'

    def dispatch(self, request, *args, **kwargs):
        if HomePage.objects.filter(page=0):
            return HttpResponseRedirect(reverse_lazy("home"))
        elif HomePage.objects.filter(page=2):
            return HttpResponseRedirect(reverse_lazy("allmarket"))
        return super().dispatch(request, *args, **kwargs)


market_view = HomeTwoView.as_view()


class HomeThirdView(ExtraContextData, PromotionMixin, generic.TemplateView):

    template_name = "combine.html"

    def dispatch(self, request, *args, **kwargs):
        if HomePage.objects.filter(page=0):
            return HttpResponseRedirect(reverse_lazy("home"))
        elif HomePage.objects.filter(page=1):
            return HttpResponseRedirect(reverse_lazy("market"))
        return super().dispatch(request, *args, **kwargs)


combine_view = HomeThirdView.as_view()


class ProductListView(FilterMixin, PromotionMixin, generic.ListView):
    model = Product
    paginate_by = 20
    extra_context = {'page_title': 'Tous les produits'}
    template_name = "catalogue/product_list.html"

    def get_context_data(self, *args, **kwargs):
        kwargs["query"] = self.request.GET.get("q", None)
        kwargs['promotions'] = self.promotions()
        kwargs['promotion_list'] = self.get_promotions_list()
        kwargs['product_recommended'] = utils.get_recently_viewed(self.request)
        return super().get_context_data(*args, **kwargs)

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        query = self.request.GET.get("q")
        if query:
            query_one = self.model.objects.filter(
                Q(name__icontains=query)
                | Q(description__icontains=query)
                | Q(price__icontains=query)
                | Q(keywords__icontains=query)
            )
            try:
                query_two = self.model.objects.filter(Q(price=query))
                qs = (query_one | query_two).distinct()
            except:
                pass
        return qs


product_list_view = ProductListView.as_view()


@csrf_exempt
def show_product(request, slug, template="catalogue/product_detail.html"):

    """
    vue pour chaque page de produit
    """
    p = get_object_or_404(Product, slug=slug)
    product_cache_key = request.path

    # essayer de récupérer le produit à partir du cache
    p = cache.get(product_cache_key)

    # si le cache manque, on se rabat sur
    # la requête de la base de données
    if not p:
        p = get_object_or_404(Product, slug=slug)
        # stocker l'élément dans le cache
        # pour la prochaine fois
        cache.set(product_cache_key, p, settings.CACHE_TIMEOUT)

    # évaluez la méthode HTTP, modifiez-la si nécessaire
    if request.method == 'POST':
        # créer le formulaire lié
        postdata = request.POST.copy()
        form = ProductAddToCartForm(request, postdata)

        # vérifier si les données affichées sont valides
        if form.is_valid():
            # ajouter au panier et rediriger
            # vers la page du panier
            cart.add_to_cart(request)

            msg = f""" '{p.name}' a été ajouté à votre panier."""
            messages.success(request, mark_safe(msg))

            # si le cookie de test a fonctionné,
            # il faut s'en débarrasser
            if request.session.test_cookie_worked():
                request.session.delete_test_cookie()
            return HttpResponseRedirect(reverse('cart:cart'))
    else:
        # créer le formulaire non lié. Remarquez la requête
        # comme un argument de mot-clé
        form = ProductAddToCartForm(request=request, label_suffix=':')

    # affiche les produits similaires
    related_product = sorted(Product.objects.get_category_related(
        instance=p)[:15], key=lambda x: random.random())

    # affiche les produits recommendés
    recommended_product = Product.objects.recomended_product(instance=p)

    # définir le cookie de test pour s'assurer
    # que les cookies sont activés
    request.session.set_test_cookie()

    # ajout d'avis sur le produit courant
    # product_review = ProductReview.objects.filter(product=p)

    # sauvegarder l'utilisateur actuel
    utils.log_product_view(request, p)

    context = {
        'page_title': p.name,
        'object': p,
        'category': Category.objects.all(),

        'form': form,
        'review_form': ProductReviewForm(),

        'related_product': related_product,
        'recommended_product': recommended_product,
        'cart_items': cart.get_cart_items(request),
        'recently_viewed': utils.get_recently_viewed(request),
    }

    return render(request, template, context)


@csrf_exempt
def addRreview(request, slug):
    product = get_object_or_404(Product, slug=slug)

    if request.method == 'POST':
        form = ProductReviewForm(request.POST or None)
        if form.is_valid():
            name = form.cleaned_data['name']
            rating = form.cleaned_data['rating']
            email = form.cleaned_data['email']
            content = form.cleaned_data['content']

            ProductReview.objects.create(
                name=name,
                email=email,
                product=product,
                content=content,
                is_approved=False,
                created_time_at=timezone.now(),
                created_hour_at=timezone.now(),
            )

            messages.success(request, "Votre avis à été ajouté avec succes. Merci pour votre intérêt.")
            return HttpResponseRedirect(product.get_absolute_url())
    return HttpResponseRedirect(product.get_absolute_url())
