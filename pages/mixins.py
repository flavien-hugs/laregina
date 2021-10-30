# pages.mixins.py

from pages.models import Promotion


class PromotionMixin(object):

	def get_promotions_list(self):
		return Promotion.objects.filter(active=True)
