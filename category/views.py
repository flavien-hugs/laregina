# category.views.py

from django.views import generic

from analytics import utils
from category.models import Category
from catalogue.models import Product


class CategoryDetailView(generic.DetailView, generic.list.MultipleObjectMixin):
    paginate_by = 20
    slug_field = "slug"
    slug_url_kwarg = "slug"
    queryset = Category.objects.all()
    template_name = "category/category_detail.html"

    def get_context_data(self, **kwargs):

        category = self.get_object().get_descendants(include_self=True)
        products = Product.objects.filter(category__in=category)
        product_recommended = utils.get_recently_viewed(self.request)

        kwargs['object_list'] = products
        kwargs['category'] = self.queryset
        kwargs['product_recommended'] = product_recommended
        kwargs['page_title'] = f"{self.object.name}"
        return super().get_context_data(**kwargs)


category_detail_view = CategoryDetailView.as_view()
