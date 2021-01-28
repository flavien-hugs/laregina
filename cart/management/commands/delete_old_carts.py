# cart.management.commands

from django.core.management.base import NoArgsCommand
from cart import cart

class Command(NoArgsCommand):
    help = "Supprimer les articles du panier d'achat datant de plus de 90 jours"
    def handle_noargs(self, **options):
        cart.remove_old_cart_items()
