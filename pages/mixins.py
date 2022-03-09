# pages.mixins.py

from pages.models import Campaign
from catalogue.models import Product


class PromotionMixin(object):

	def get_promotions_list(self):
		return Campaign.objects.published()
