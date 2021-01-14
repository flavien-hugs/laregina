# catalogue.views.py

from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView

from category.models import Category
from catalogue.models import Product, ProductImage


# PRODUCT LIST VIEW
class ProductListView(ListView):
    paginate_by = 50
    queryset = Product.objects.all()
    template_name = "catalogue/product_list.html"


# PRODUCT LIST VIEW
class ProductDetailView(DetailView):
    model = Product
    template_name = "catalogue/product_detail.html"
    success_url = reverse_lazy('catalogue:product_detail')

    def get_context_data(self, **kwargs):
        obj = self.get_object()
        kwargs['page_title'] = self.object.name
        kwargs['category'] = Category.objects.all()
        kwargs['product_image'] = ProductImage.objects.filter(product_id=obj.id)

        # Affiche les produits similaires
        kwargs['related_product'] = Product.objects.get_related(instance=obj)[:15]

        return super().get_context_data(**kwargs)
