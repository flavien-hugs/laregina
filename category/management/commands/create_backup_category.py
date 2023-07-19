# category.management.commands.create_backup_category.py
from category.models import Category
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Affiche la liste des catégorie."

    def handle(self, *args, **options):
        backup_category = Category.objects.all()

        for cat in backup_category:
            self.stdout.write(cat.name)
