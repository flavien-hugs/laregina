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
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
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

CACHE_TTL = getattr(settings, 'CACHE_TTL', settings.CACHE_TIMEOUT)


class ExtraContextData:

    queryset = Category.objects.all()

    def get_context_data(self, **kwargs):
        kwargs['promotions'] = self.get_promotions()
        kwargs['destockages'] = self.get_destockages()
        kwargs['sales_flash'] = self.get_sales_flash()
        kwargs['news_arrivals'] = self.get_news_arrivals()

        kwargs['promotion_list'] = self.get_promotions_list()[:6]
        kwargs['vendor_list'] = get_list_or_404(get_user_model())[0:8]
        kwargs['recently_viewed'] = utils.get_recently_viewed(request=self.request)
        kwargs['category_list'] = self.queryset

        category = self.queryset
        kwargs['products'] = Product.objects\
            .prefetch_related("category")\
            .filter(category__parent__in=category)[:15]

        return super().get_context_data(**kwargs)


class HomeThirdView(ExtraContextData, PromotionMixin, generic.TemplateView):

    template_name = "combine.html"


combine_view = HomeThirdView.as_view()


"""
class HomeView(ExtraContextData, PromotionMixin, generic.TemplateView):

    template_name = "index.html"

    @method_decorator(cache_page(CACHE_TTL))
    def dispatch(self, request, *args, **kwargs):
        if HomePage.objects.filter(page=1):
            return HttpResponseRedirect(reverse_lazy("market"))
        elif HomePage.objects.filter(page=2):
            return HttpResponseRedirect(reverse_lazy("allmarket"))
        return super().dispatch(request, *args, **kwargs)


home_view = HomeView.as_view()


@method_decorator(cache_page(CACHE_TTL),  name='dispatch')
class HomeMarketView(PromotionMixin, generic.TemplateView):

    template_name = "market.html"
    try:
        queryset = Category.objects.get(pk=223)
    except:
        queryset = Category.objects.all()

    def get_context_data(self, **kwargs):
        categories = self.queryset.get_children()
        kwargs['farm'] = categories[:15]
        return super().get_context_data(**kwargs)


home_market_view = HomeMarketView.as_view()


class HomeTwoView(ExtraContextData, PromotionMixin, generic.TemplateView):

    template_name = 'market.html'

    @method_decorator(cache_page(CACHE_TTL))
    def dispatch(self, request, *args, **kwargs):
        if HomePage.objects.filter(page=0):
            return HttpResponseRedirect(reverse_lazy("home"))
        elif HomePage.objects.filter(page=2):
            return HttpResponseRedirect(reverse_lazy("allmarket"))
        return super().dispatch(request, *args, **kwargs)


market_view = HomeTwoView.as_view()
"""

@method_decorator(cache_page(CACHE_TTL),  name='dispatch')
class ProductListView(FilterMixin, PromotionMixin, generic.ListView):
    paginate_by = 15
    queryset = Product.objects.all()
    extra_context = {'page_title': 'Tous les produits'}
    template_name = "catalogue/product_list.html"

    def get_context_data(self, *args, **kwargs):
        kwargs["query"] = self.request.GET.get("q", None)
        kwargs['promotions'] = self.get_promotions()
        kwargs['promotion_list'] = self.get_promotions_list()
        kwargs['product_recommended'] = utils.get_recently_viewed(self.request)
        return super().get_context_data(*args, **kwargs)

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        query = self.request.GET.get("q")
        if query:
            query_one = self.queryset.filter(
                Q(name__icontains=query)
                | Q(description__icontains=query)
                | Q(price__icontains=query)
                | Q(keywords__icontains=query)
                | Q(category__slug__icontains=query)
            )
            try:
                query_two = self.queryset.filter(Q(price=query))
                qs = (query_one | query_two).distinct()
            except:
                pass
        return qs


product_list_view = ProductListView.as_view()


@csrf_exempt
def show_product(request, slug, pk, template="catalogue/product_detail.html"):
    p = get_object_or_404(Product, slug=slug, pk=pk)
    product_cache_key = request.path
    p = cache.get(product_cache_key)
    if not p:
        p = get_object_or_404(Product, slug=slug, pk=pk)
        cache.set(product_cache_key, p, settings.CACHE_TIMEOUT)
    if request.method == 'POST':
        postdata = request.POST.copy()
        form = ProductAddToCartForm(request, postdata)
        if form.is_valid():
            cart.add_to_cart(request)

            msg = f""" '{p.name}' a été ajouté à votre panier."""
            messages.success(request, mark_safe(msg))
            if request.session.test_cookie_worked():
                request.session.delete_test_cookie()
            return HttpResponseRedirect(reverse('cart:cart'))
    else:
        form = ProductAddToCartForm(request=request, label_suffix=':')
    related_product = sorted(Product.objects.get_category_related(
        instance=p)[:15], key=lambda x: random.random())
    recommended_product = Product.objects.recomended_product(instance=p)
    request.session.set_test_cookie()
    utils.log_product_view(request, p)

    context = {
        'object': p,
        'page_title': p.name,
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
def add_review(request, slug):
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
