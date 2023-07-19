from django.conf import settings
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.urls import reverse

from ..forms import DistributorCustomerForm
from ..models import DistributorCustomer


def distributorRegisterView(request, template="account/customer/register.html"):
    form = DistributorCustomerForm()
    if request.method == "POST":
        form = DistributorCustomerForm(request.POST or None)
        if form.is_valid():
            delivery = form.save()
            messages.success(
                request,
                "Merci pour votre inscription, nous vous contacterons plus tard pour valider votre compte.",
            )
            success_url = reverse(
                "delivery:delivery_register_success",
                kwargs={"delivery_id": delivery.delivery_id},
            )
            request.session["delivery_id"] = str(delivery.delivery_id)
            return HttpResponseRedirect(success_url)
        messages.error(request, "Veuillez vérifier les informations fournies !")

    context = {"form": form, "page_title": "S'inscrire en tant que distributeur"}
    return render(request, template, context)


distributor_register_view = distributorRegisterView


def distributorRegisterSuccessView(
    request, delivery_id, template="account/customer/success_register.html"
):
    delivery_id = request.session.get("delivery_id")
    delivery = get_object_or_404(DistributorCustomer, delivery_id=delivery_id)
    message = f"Bonjour {settings.SITE_NAME}, je viens de m'inscrire en tant que distributeur."
    context = {
        "object": delivery,
        "message": message,
        "page_title": "Inscription validée",
    }
    return render(request, template, context)


distributor_register_success_view = distributorRegisterSuccessView
