# accounts/mixins.py

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from accounts.models import UserProfile


class CreateWithOwnerMixin(LoginRequiredMixin):
    """
    Injecte l'utilisateur actuellement connecté dans le champ
    "propriétaire" du formulaire dans cette vue.
    """

    # TODO: Déterminer la meilleure mise en œuvre
    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        form.instance.owner = UserProfile.objects.get(user=self.request.user)
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


class CreateWithReviewerMixin(LoginRequiredMixin):
    """
    Injecte l'utilisateur actuellement connecté dans le champ
    "réviseur" du formulaire dans cette vue.
    """
    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        form.instance.reviewer = UserProfile.objects.get(user=self.request.user)
        return form


class CreateWithSenderMixin(LoginRequiredMixin):
    """
    Injecte l'utilisateur actuellement connecté dans le champ
    "expéditeur" du formulaire dans cette vue.
    """
    # TODO: Déterminer la meilleure mise en œuvre
    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        form.instance.sender = UserProfile.objects.get(user=self.request.user)
        return form


class OwnerRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """
    Limite l'accès à cette vue à l'utilisateur qui est le
    propriétaire de cet objet (dans une vue d'objet unique).
    """
    # TODO: Augmenter de 404 au lieu de 503
    raise_exception = True

    def test_func(self):
        # Suppose que ceci a un attribut get_object
        # Pourrait être testé avec hasattr() ?
        return self.request.user == self.get_object().owner


class SellerRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """
    Limite l'accès à cette vue aux utilisateurs du groupe Vendeur.
    """
    # TODO:Augmenter de 404 au lieu de 503
    raise_exception = True

    def test_func(self):
        # TODO: Utilisez plutôt des groupes d'utilisateurs
        # return self.request.user.groups.filter(name='Seller').exists()
        return self.request.profile.is_seller
