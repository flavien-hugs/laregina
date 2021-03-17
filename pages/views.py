# pages.views.py

from django.contrib import messages
from django.views.generic import View
from django.shortcuts import render, redirect

from pages.forms import ContactForm


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
