# pages.views.py

from django.contrib import messages
from django.views.generic import View
from django.shortcuts import render, redirect

from pages.forms import ContactForm, PromotionForm


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
        form = ContactForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request, "Votre message a été envoyé avec success.")
        return redirect('pages:contact')


class PromotionView(View):
    form_class = PromotionForm
    template_name = "pages/promotion.html"

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        ctx = {
            'form': form,
            'page_title': 'Ajouter une afficher pour la promotion de votre boutique',
        }
        return render(request, self.template_name, ctx)

    def post(self, request, *args, **kwargs):
        form = PromotionForm(request.POST or None, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Votre promotion a été envoyé avec success !")
        return redirect('pages:promotion')
