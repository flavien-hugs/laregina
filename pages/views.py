# pages.views.py

from django.views import generic
from django.contrib import messages
from django.shortcuts import render, redirect


from analytics import utils
from pages import models, forms, mixins


class ContactView(generic.View):
    form_class = forms.ContactForm
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


class PromotionView(generic.View):
    form_class = forms.PromotionForm
    template_name = "pages/promotion/form.html"

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


class PromotionDetailView(mixins.PromotionMixin, generic.DetailView):
    model = models.Promotion
    paginate_by = 50
    template_name = "pages/promotion/promotion_list.html"

    def get_context_data(self, *args, **kwargs):
        kwargs["page_title"] = self.object.name
        kwargs['promotion_list'] = self.get_promotions_list()
        kwargs['product_recommended'] = utils.get_recently_viewed(self.request)
        return super().get_context_data(*args, **kwargs)


promotion_detail = PromotionDetailView.as_view()
