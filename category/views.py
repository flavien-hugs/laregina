# category.views.py

from django.views import generic

from analytics import utils
from category.models import Category
from catalogue.models import Product

from pages.mixins import PromotionMixin


class CategoryDetailView(
    PromotionMixin, generic.DetailView,
    generic.list.MultipleObjectMixin):

    model = Category
    paginate_by = 20
    slug_field = "slug"
    slug_url_kwarg = "slug"
    queryset = Category.objects.all()
    template_name = "catalogue/product_list.html"

    def get_queryset(self):
        return self.model.objects.all()

    def get_context_data(self, **kwargs):
        kwargs['page_title'] = self.object.name
        kwargs['object_list'] = Product.objects.filter(
            category__in=self.object.get_descendants(include_self=True)
        )
        kwargs['product_recommended'] = utils.get_recently_viewed(self.request)
        return super().get_context_data(**kwargs)


category_detail_view = CategoryDetailView.as_view()
