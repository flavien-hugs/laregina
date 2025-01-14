from analytics import utils
from catalogue.models import Product
from category.models import Category
from django.conf import settings
from django.views import generic
from pages.mixins import PromotionMixin

CACHE_TTL = getattr(settings, "CACHE_TTL", settings.CACHE_TIMEOUT)


# @method_decorator(cache_page(CACHE_TTL), name="dispatch")
class CategoryDetailView(
    PromotionMixin, generic.DetailView, generic.list.MultipleObjectMixin
):
    model = Category
    paginate_by = 16
    slug_field = "slug"
    queryset = Category.objects.all()
    template_name = "catalogue/product_list.html"

    def get_queryset(self):
        return self.queryset

    def get_context_data(self, **kwargs):
        category_object = self.object.get_descendants(include_self=True)
        kwargs["page_title"] = self.object.name
        kwargs["object_list"] = Product.objects.prefetch_related("category").filter(
            category__in=category_object
        )
        kwargs["product_recommended"] = utils.get_recently_viewed(self.request)
        return super().get_context_data(**kwargs)


category_detail_view = CategoryDetailView.as_view()
