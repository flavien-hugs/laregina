from catalogue.models import Product
from category.models import Category
from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = "daily"

    def items(self):
        return [
            "home",
            "pages:about-us",
            "pages:faqs",
            "pages:cgu",
            "pages:policy",
            "pages:return",
            "pages:contact",
        ]

    def location(self, item):
        return reverse(item)


class CategorySitemapView(Sitemap):
    changefreq = "always"
    priority = 0.7

    def items(self):
        return Category.objects.all()

    def location(self, item):
        return item.get_absolute_url()


class ProductSitemapView(Sitemap):
    changefreq = "always"
    priority = 0.7

    def items(self):
        return Product.objects.all()

    def location(self, item):
        return item.get_absolute_url()


SITEMAPS = {
    "static": StaticViewSitemap,
    "category": CategorySitemapView,
    "product": ProductSitemapView,
}
