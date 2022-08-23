# category.views.py

from django.views import generic

from analytics import utils
from category.models import Category
from catalogue.models import Product

from pages.mixins import PromotionMixin


class CategoryDetailView(
    PromotionMixin, generic.DetailView,
    generic.list.MultipleObjectMixin):

    paginate_by = 20
    slug_field = "slug"
    slug_url_kwarg = "slug"
    queryset = Category.objects.all()
    template_name = "category/category_detail.html"

    def get_context_data(self, **kwargs):
        kwargs['category'] = self.queryset
        kwargs['page_title'] = self.object.name
        kwargs['object_list'] = self.get_object().get_products_in_category()
        kwargs['product_recommended'] = utils.get_recently_viewed(self.request)
        return super().get_context_data(**kwargs)


category_detail_view = CategoryDetailView.as_view()
