# catalogue.signals.py
from django.dispatch import Signal

product_viewed = Signal(providing_args=["product", "user", "request", "response"])
