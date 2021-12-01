# pages.views.py

from django.views import generic
from django.contrib import messages
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404, render, redirect

from analytics import utils
from pages import models, forms, mixins
from accounts.mixins import SellerRequiredMixin


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


contact_view = ContactView.as_view()


@login_required
def promotion_create_view(
    request,
    template="dashboard/seller/includes/_partials_promotion_form.html"
):
    if request.method == 'POST':
        form = forms.PromotionForm(request.user, request.POST or None, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.user = request.user
            product.save()
            messages.success(request, "Votre promotion a été ajouté avec success !")
            return redirect('seller:promotion_list')
    else:
        form = forms.PromotionForm(request.user)

    context = {
        'form': form,
        'page_title': 'créer une promotion',
        'subtitle': 'créer une promotion',
    }
    return render(request, template, context)


promotion_view = promotion_create_view


class PromotionListView(
    SellerRequiredMixin,
    mixins.PromotionMixin, generic.ListView
):
    model = models.Promotion
    paginate_by = 10
    template_name = "dashboard/seller/includes/_partials_promotion.html"

    def get_queryset(self):
        return self.get_prompotion()

    def get_context_data(self, *args, **kwargs):
        kwargs["subtitle"] = "promotions"
        kwargs["page_title"] = "liste de vos promotions"
        return super().get_context_data(*args, **kwargs)


promotion_list = PromotionListView.as_view()


class PromotionDetailView(mixins.PromotionMixin, generic.DetailView):
    model = models.Promotion
    paginate_by = 25
    template_name = "dashboard/seller/includes/_partials_promotion_list.html"

    def get_context_data(self, *args, **kwargs):
        kwargs["page_title"] = self.object.name
        kwargs['promotion_list_object'] = self.get_promotions_list()
        kwargs['product_recommended'] = utils.get_recently_viewed(self.request)
        return super().get_context_data(*args, **kwargs)


promotion_detail = PromotionDetailView.as_view()


@login_required
def promotion_update_view(
    request, slug,
    template="dashboard/seller/includes/_partials_promotion_form.html"
):
    obj = get_object_or_404(models.Promotion, slug=slug)
    form = forms.PromotionForm(
        request.user,
        request.POST or None,
        instance=obj
    )
    if form.is_valid():
        form.save()
        msg = f'Mise à jour de la promotion "{obj.product.name}" effectuée avec succes !'
        messages.success(request, msg)
        return redirect("seller:promotion_list")
 
    context = {
        'form': form,
        'page_title': 'mise à jour de la promotion',
        'subtitle': 'mise à jour promotion',
    }
 
    return render(request, template, context)


promotion_update = promotion_update_view


class PromotionDeleteView(
    SellerRequiredMixin,
    SuccessMessageMixin,
    generic.DeleteView
):
    model = models.Promotion
    form_class = forms.PromotionForm
    success_message = 'Suppression de la promotion effectuée avec succes !'
    success_url = reverse_lazy('seller:promotion_list')

    def form_valid(self, form):
        return HttpResponseRedirect(self.get_success_url())


promotion_delete = PromotionDeleteView.as_view()