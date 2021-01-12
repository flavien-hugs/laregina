# accounts/mixins.py

import datetime
from django.db.models import Sum, Avg
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from catalogue.models import Product

User = get_user_model()


class CustomerWithOwnerMixin(LoginRequiredMixin):
    """
        Injecte l'utilisateur actuellement connecté dans le champ propriétaire du formulaire dans cette vue.
    """

    # TODO: Déterminer la meilleure mise en œuvre
    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        form.instance.user = User.objects.get(user=self.request.user)
        return form

    # def get_form_kwargs(self):
    #     kwargs = super().get_form_kwargs()
    #     # Update the forms kwargs with the current UserProfile
    #     # kwargs['instance'].owner = UserProfile.objects.get(user=self.request.user)
    #     # kwargs.update({'owner': UserProfile.objects.get(user=self.request.user)})
    #     return kwargs

    # def form_valid(self, form):
    #     form.instance.owner = UserProfile.objects.get(user=self.request.user)
    #     return super().form_valid(form)


# class CreateWithReviewerMixin(LoginRequiredMixin):
#     """
#     Injecte l'utilisateur actuellement connecté dans le champ
#     "réviseur" du formulaire dans cette vue.
#     """
#     def get_form(self, *args, **kwargs):
#         form = super().get_form(*args, **kwargs)
#         form.instance.reviewer = User.objects.get(user=self.request.user)
#         return form


# class CreateWithSenderMixin(LoginRequiredMixin):
#     """
#     Injecte l'utilisateur actuellement connecté dans le champ
#     "expéditeur" du formulaire dans cette vue.
#     """
#     # TODO: Déterminer la meilleure mise en œuvre
#     def get_form(self, *args, **kwargs):
#         form = super().get_form(*args, **kwargs)
#         form.instance.sender = User.objects.get(user=self.request.user)
#         return form


class CustomerRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """
        Limite l'accès à cette vue à l'utilisateur qui est
        le propriétaire de cet objet (dans une vue d'objet unique).
    """

    # TODO: Augmenter de 404 au lieu de 503
    raise_exception = True

    def test_func(self):
        # Suppose que ceci a un attribut get_object ourrait être testé avec hasattr() ?
        return self.request.user.is_buyer


class SellerRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """
        Limite l'accès de cette vue aux utilisateurs du groupe Vendeur.
    """

    # TODO:Augmenter de 404 au lieu de 503
    raise_exception = True

    def test_func(self):
        # TODO: Utilisez plutôt des groupes d'utilisateurs
        # return self.request.user.groups.filter(name='Vendeur').exists()
        return self.request.user.is_seller


class UserAccountMixin(LoginRequiredMixin, object):
    product = []

    def get_user_product(self):
        product = Product.objects.filter(user=self.get_account())
        self.product = product
        return product

    # def get_user_payment(self):
    #     payment = Payment.objects.filter(product__in=self.get_product())
    #     return payment

    # def get_payment_today(self):
    #     today = datetime.date.today()
    #     today_min = datetime.datetime.combine(today, datetime.time.min)
    #     today_max = datetime.datetime.combine(today, datetime.time.max)
    #     return self.get_payment().filter(created__range=(today_min, today_max))

    # def get_total_sale(self):
    #     payment = self.get_payment().aggregate(Sum("price"))
    #     total_sale = payment["price__sum"]
    #     return total_sale

    # def get_today_sale(self):
    #     payment = self.get_payment_today().aggregate(Sum("price"), Avg("price"))
    #     total_sale = payment["price__sum"]
    #     return total_sale