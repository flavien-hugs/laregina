import random

from pages.models import Campaign


class PromotionMixin(object):
    def get_promotions_list(self):
        return Campaign.objects.published()

    def get_promotions(self):
        return Campaign.objects.ventes_flash()

    def get_destockages(self):
        destockages = sorted(
            Campaign.objects.destockages()[:15], key=lambda x: random.random()
        )
        return destockages

    def get_sales_flash(self):
        sales_flash = sorted(
            Campaign.objects.ventes_flash()[:15], key=lambda x: random.random()
        )
        return sales_flash

    def get_news_arrivals(self):
        news = sorted(
            Campaign.objects.nouvelle_arrivages()[:15], key=lambda x: random.random()
        )
        return news
