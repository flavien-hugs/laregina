# category.views.py

from django.views import generic

from analytics import utils
from category.models import Category
from catalogue.models import Product


class CategoryDetailView(generic.DetailView):
    model = Category
    paginate_by = 20
    template_name = "category/category_detail.html"

    def get_queryset(self):
        return Category.objects.all()

    def get_context_data(self, **kwargs):
        obj = self.get_object().get_descendants(include_self=True)
        kwargs['object_list'] = Product.objects.filter(category__in=obj)
        kwargs['category'] = self.model.objects.all()
        kwargs['product_recommended'] = utils.get_recently_viewed(self.request)
        kwargs['page_title'] = 'Catégories: {category_name}'.format(
            category_name=self.object.name)
        return super().get_context_data(**kwargs)
