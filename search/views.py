# search.views.py

from itertools import chain
from django.urls import reverse_lazy
from django.views.generic import ListView

from search import search
from catalogue.models import Product
from category.models import Category


class SearchView(ListView):
    template_name = 'catalogue/product_list.html'
    success_url = reverse_lazy('search')
    paginate_by = 50
    
    def get_context_data(self, *args, **kwargs):
        query = self.request.GET.get('q', None)
        kwargs['page_title'] = 'Résultat de recherche pour : "{}"'.format(query)
        return super().get_context_data(*args, **kwargs)

    def get_queryset(self, *args, **kwargs):
        query = self.request.GET.get('q', None)
        search.store(self.request, query)
        return search.products(query).get('products', [])
