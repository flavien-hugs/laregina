# category.views.py

from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView

from catalogue.models import Product
from category.models import Category


# LIST CATEGORY VIEW
class CategoryListView(ListView):
    queryset = Category.objects.all()
    template_name = "category/category_list.html"
    extra_context = {'page_title': 'toutes les catégories de produit'}

    def get_context_data(self, **kwargs):
        obj = self.queryset.get_descendants(include_self=True)
        kwargs['object_list'] = Product.objects.filter(categories__in=obj)
        return super().get_context_data(**kwargs)


# DETAIL CATEGORY VIEW
class CategoryDetailView(DetailView):
    queryset = Category.objects.all()
    template_name = "category/category_detail.html"
    paginate_by = 50

    def get_context_data(self, **kwargs):
        obj = self.get_object().get_descendants(include_self=True)
        kwargs['object_list'] = Product.objects.filter(category__in=obj)
        kwargs['category'] = self.queryset
        kwargs['page_title'] = '{category_name}'.format(category_name=self.object.name)
        return super().get_context_data(**kwargs)
