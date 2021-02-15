# pages.views.py

from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.generic import View, CreateView, TemplateView

from pages.models import Subscribe
from pages.forms import ContactForm
from core.utils import SendSubscribeMail


def subscribeView(request):
    if request.method == "POST":
        email = request.POST["email"]
        email_qs = Subscribe.objects.filter(email=email)
        if email_qs.exists():
            messages.success(
                request, "Désolé cette adresse existe déjà comme abonné.")
            return JsonResponse({"success": True}, status=200)
        else:
            Subscribe.objects.create(email=email)
            messages.success(request, "Super ! vous êtes désormais un abonné.")
            SendSubscribeMail(email)
    return JsonResponse({"success": False}, status=400)


class ContactView(View):
    form_class = ContactForm
    template_name = "pages/contact.html"

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        ctx = {
            'form': form,
            'page_title': 'Contactez-nous',
            'page_description': "Comment pouvons-nous aider ?"
        }
        return render(request, self.template_name, ctx)

    def post(self, request, *args, **kwargs):
        if self.request.method == "POST" and self.request.is_ajax():
            form = self.form_class(request.POST)
            form.save()
            messages.success(request, "Votre message a été envoyé avec success.")
            return JsonResponse({"success":True}, status=200)
        return JsonResponse({"success":False}, status=400)
