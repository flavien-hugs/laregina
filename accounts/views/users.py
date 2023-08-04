from django.views import generic
from django.contrib import messages
from django.shortcuts import render
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin

from checkout.models import Order
from accounts.forms import AccountUpdateForm
from accounts.mixins import CustomerRequiredMixin


@login_required(login_url="accounts:account_login")
def account_dashboard(request):
    context = {"page_title": "Votre compte"}

    return render(request, "dashboard/users/index.html", context)


dashboard_view = account_dashboard


class SettingsUpdateView(
    CustomerRequiredMixin, SuccessMessageMixin, generic.UpdateView
):
    slug_field = "slug"
    model = get_user_model()
    form_class = AccountUpdateForm
    success_message = "Votre profile a été mise à jour avec succes !"
    template_name = "dashboard/users/includes/_partials_settings_store.html"

    def get_object(self, *args, **kwargs):
        return self.get_account()

    def get_context_data(self, *args, **kwargs):
        kwargs["subtitle"] = "Réglages"
        kwargs["page_title"] = f"Configuration de votre boutique : {self.object.store}"
        return super().get_context_data(*args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()

        msg = "Votre profile a été mise à jour avec succes !"
        messages.success(self.request, msg)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy(
            "dashboard_seller:update", kwargs={"slug": self.get_object().slug}
        )


settings_view = SettingsUpdateView.as_view()


class OrderListView(CustomerRequiredMixin, generic.ListView):
    paginate_by = 10
    template_name = "dashboard/users/includes/_partials_orders_list.html"

    def get_object(self, *args, **kwargs):
        return self.get_account()

    def get_queryset(self):
        return self.get_order_items()

    def get_context_data(self, **kwargs):
        kwargs["subtitle"] = "vos commandes"
        kwargs["page_title"] = "liste des vos commandes"
        return super().get_context_data(**kwargs)


order_list_view = OrderListView.as_view()


class OrderDetailView(CustomerRequiredMixin, generic.DetailView):
    model = Order
    template_name = "dashboard/users/includes/_partials_orders_detail.html"

    def get_context_data(self, **kwargs):
        kwargs["subtitle"] = "commande"
        kwargs["page_title"] = f"commande N°: {self.object.transaction_id}"
        return super().get_context_data(**kwargs)


order_detail_view = OrderDetailView.as_view()
