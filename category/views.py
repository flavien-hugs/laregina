# category.views.py

from django.http import Http404
from django.db import connection
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, TemplateView

from catalogue.forms import VariationInventoryFormSet
from django_filters import FilterSet, CharFilter, NumberFilter

from category.models import Category
from catalogue.models import Product, Variation


# LIST CATEGORY VIEW
class CategoryListView(ListView):
    model = Category
    paginate_by = 50
    template_name = "category/category_list.html"
    extra_context = {'page_title': 'toutes les catégories de produit'}

    def get_context_data(self, **kwargs):
        obj = self.queryset.get_descendants(include_self=True)
        kwargs['queries'] = connection.queries
        kwargs['object_list'] = Product.objects.filter(category__in=obj)
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        from django.db import connection
        queries = connection.queries
        return Category.objects.all()


# DETAIL CATEGORY VIEW
class CategoryDetailView(DetailView):
    model = Category
    template_name = "category/category_detail.html"

    def get_context_data(self, **kwargs):
        obj = self.get_object().get_descendants(include_self=True)
        kwargs['object_list'] = Product.objects.filter(category__in=obj)
        kwargs['category'] = self.model.objects.all()
        kwargs['page_title'] = '{category_name}'.format(category_name=self.object.name)
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        from django.db import connection
        queries = connection.queries
        return Category.objects.all()


class VariationListView(ListView):
    model = Variation
    queryset = Variation.objects.all()

    def get_context_data(self, *args, **kwargs):
        context["formset"] = VariationInventoryFormSet(queryset=self.get_queryset())
        return super(VariationListView, self).get_context_data(*args, **kwargs)

    def get_queryset(self, *args, **kwargs):
        product_pk = self.kwargs.get("pk")
        if product_pk:
            product = get_object_or_404(Product, pk=product_pk)
            queryset = Variation.objects.filter(product=product)
        return queryset

    def post(self, request, *args, **kwargs):
        formset = VariationInventoryFormSet(request.POST, request.FILES)
        if formset.is_valid():
            formset.save(commit=False)
            for form in formset:
                new_item = form.save(commit=False)
                product_pk = self.kwargs.get("pk")
                product = get_object_or_404(Product, pk=product_pk)
                new_item.product = product
                new_item.save()
                
            messages.success(request, "Votre inventaire et votre tarification ont été mis à jour.")
            return redirect("/")
        raise Http404
