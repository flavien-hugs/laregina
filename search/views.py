# search.views.py

from django.views import generic
from django.urls import reverse_lazy

from search import search


class SearchView(generic.ListView):
    paginate_by = 50
    success_url = reverse_lazy('search')
    template_name = 'catalogue/product_list.html'
    
    def get_context_data(self, *args, **kwargs):
        query = self.request.GET.get('q', None)
        kwargs['page_title'] = f'Résultat de recherche pour : "{query}"'
        return super().get_context_data(*args, **kwargs)

    def get_queryset(self, *args, **kwargs):
        query = self.request.GET.get('q', None)
        search.store(self.request, query)
        return search.products(query).get('products', [])


search_view = SearchView.as_view()
