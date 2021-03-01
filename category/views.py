# category.views.py

from django.views.generic import DetailView

from category.models import Category
from catalogue.models import Product


# DETAIL CATEGORY VIEW
class CategoryDetailView(DetailView):
    model = Category
    template_name = "category/category_detail.html"

    def get_context_data(self, **kwargs):
        obj = self.get_object().get_descendants(include_self=True)
        kwargs['object_list'] = Product.objects.filter(category__in=obj)
        kwargs['category'] = self.model.objects.all()
        kwargs['page_title'] = 'Catégories: {category_name}'.format(
            category_name=self.object.name)
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        from django.db import connection
        queries = connection.queries
        return Category.objects.all()
