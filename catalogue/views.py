# catalogue.views.py

import json
import random
from django.db.models import Q
from django.urls import reverse
from django.utils import timezone
from django.contrib import messages
from django.core.cache import cache
from django.views.generic import ListView
from django.utils.safestring import mark_safe
from django.shortcuts import render, get_object_or_404
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponseRedirect, HttpResponse

from cart import cart
from analytics import utils
from category.models import Category
from core.settings import CACHE_TIMEOUT
from catalogue.forms import ProductAddToCartForm
from catalogue.models import Product, ProductImage

from reviews.models import ProductReview
from reviews.forms import ProductReviewForm


class FilterMixin(object):
    filter_class = None
    search_ordering_param = "ordering"

    def get_queryset(self, *args, **kwargs):
        try:
            qs = super(FilterMixin, self).get_queryset(*args, **kwargs)
            return qs
        except:
            raise ImproperlyConfigured("Vous devez disposer d'un queryset pour pouvoir utiliser le FilterMixin")

    def get_context_data(self, *args, **kwargs):
        qs = self.get_queryset()
        ordering = self.request.GET.get(self.search_ordering_param)
        if ordering:
            qs = qs.order_by(ordering)
        filter_class = self.filter_class
        if filter_class:
            f = filter_class(self.request.GET, queryset=qs)
            kwargs["object_list"] = f
        return super(FilterMixin, self).get_context_data(*args, **kwargs)


# PRODUCT LIST VIEW
class ProductListView(FilterMixin, ListView):
    paginate_by = 50
    model = Product
    queryset = Product.objects.all()
    extra_context = {'page_title': 'Tous les produits'}
    template_name = "catalogue/product_list.html"

    def get_context_data(self, *args, **kwargs):
        kwargs["now"] = timezone.now()
        kwargs["query"] = self.request.GET.get("q", None)
        return super(ProductListView, self).get_context_data(*args, **kwargs)

    def get_queryset(self, *args, **kwargs):
        qs = super(ProductListView, self).get_queryset(*args, **kwargs)
        query = self.request.GET.get("q")
        if query:
            qs = self.model.objects.filter(
                Q(name__icontains=query) | Q(description__icontains=query)
            )
            try:
                qs2 = self.model.objects.filter(Q(price=query))
                qs = (qs | qs2).distinct()
            except:
                pass
        return qs


def show_product(request, slug, template="catalogue/product_detail.html"):
    
    """
    vue pour chaque page de produit
    """
    p = get_object_or_404(Product, slug=slug)

    # renvoie du nombre de fois le produit est visité
    nb_view = int(p.nb_view)
    nb_view += 1

    product_cache_key = request.path
    
    # essayer de récupérer le produit à partir du cache
    p = cache.get(product_cache_key)
    
    # si le cache manque, on se rabat sur
    # la requête de la base de données
    if not p:
        p = get_object_or_404(Product, slug=slug)
        # stocker l'élément dans le cache
        # pour la prochaine fois
        cache.set(product_cache_key, p, CACHE_TIMEOUT)

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
            
            msg = """
            Vous avez ajouté l'article "{product}" à votre panier.
            """.format(product=p.name)
            
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
    
    # attribuer à l'entrée cachée le slug du produit
    # form.fields['slug'].widget.attrs['value'] = slug

    # affiche les produits similaires
    similar_product = sorted(Product.objects.get_related(
        instance=p)[:15], key=lambda x: random.random())
    
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
        'product_image': ProductImage.objects.filter(product_id=p.id),
        
        'form': form,
        'review_form': ProductReviewForm(),
        # 'product_review': product_review,

        'cart_items': cart.get_cart_items(request),
        'related_product': similar_product,
        'recently_viewed': utils.get_recently_viewed(request),
        'recommended_product': utils.recommended_from_views(request)
    }

    return render(request, template, context)


def addRreview(request, slug):
    
    """
    Vue AJAX qui prend le formulaire POST d'un utilisateur soumettant
    une nouvelle évaluation de produit; nécessite un slug de produit
    valide et des args d'une instance de ProductReviewForm;
    renvoie une réponse JSON contenant deux variables : "review",
    qui contient le modèle rendu de l'évaluation du produit pour
    mettre à jour la page du produit, et "success", une valeur 
    Vrai/Faux indiquant si la sauvegarde a réussi.
    """

    product = get_object_or_404(Product, slug=slug)
    
    # review posted
    if request.method == 'POST':
        form = ProductReviewForm(request.POST or None)
        if form.is_valid():
            # Assign the current product to the review
            rating = form.cleaned_data['rating']
            email = form.cleaned_data['email']
            content = form.cleaned_data['content']
            
            ProductReview.objects.create(
                user=request.user,
                rating=rating,
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



def addProductRreview(request):

    form = ProductReviewForm(request.POST or None)
    
    # review posted
    if form.is_valid():
        # Assign the current product to the review
        review = form.save(commit=False)
        slug = request.POST.get('slug')
        product = Product.objects.get(slug=slug)
        review.user = request.user
        review.product = product
        review.save()
        messages.success(request, "Votre avis à été ajouté avec succes. Merci pour votre intérêt.")    
        
        template = 'includes/partials/_partials_product_review.html'
        ctx = {'review': review}
        html = render_to_string(template, ctx)
        response = json.dumps({'succes': 'True', 'html': html})
    else:
        html = form.errors.as_ul()
        response = json.dumps({'success': 'False', 'html': html})        
    return HttpResponse(
        response,
        content_type='application/javascript; charset=utf-8'
    )
