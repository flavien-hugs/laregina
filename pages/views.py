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
        form = forms.PromotionForm(
            request.user, request.POST or None,
            request.FILES
        )
        if form.is_valid():
            promotion = form.save(commit=False)
            promotion.user = request.user
            product = form.cleaned_data.get('products')
            promotion.save()
            promotion.products.add(*product)
            messages.success(
                request, "Votre promotion a été ajouté avec success !"
            )
            return redirect('seller:promotion_list')
        else:
            messages.error(
                request, "Vérifier les informations fournies !"
            )
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
        return self.get_promotion()

    def get_context_data(self, *args, **kwargs):
        kwargs["subtitle"] = "promotions"
        kwargs["page_title"] = "liste de vos promotions"
        return super().get_context_data(*args, **kwargs)


promotion_list = PromotionListView.as_view()


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
        msg = f'Mise à jour de la promotion "{obj.campaign.name}" effectuée avec succes !'
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
    SellerRequiredMixin, SuccessMessageMixin,
    generic.DeleteView
):
    model = models.Promotion
    form_class = forms.PromotionForm
    success_message = 'Suppression de la promotion effectuée avec succes !'
    success_url = reverse_lazy('seller:promotion_list')

    def form_valid(self, form):
        return HttpResponseRedirect(self.get_success_url())


promotion_delete = PromotionDeleteView.as_view()


class PromotionDetailView(
    mixins.PromotionMixin, generic.DetailView,
    generic.list.MultipleObjectMixin
):
    paginate_by = 25
    slug_field = "slug"
    model = models.Promotion
    slug_url_kwarg = "slug"
    template_name = "pages/promotion/_detail.html"

    def get_queryset(self):
        return self.model.objects.all()

    def get_context_data(self, *args, **kwargs):
        kwargs["page_title"] = self.object.campaign.name

        kwargs['object_list'] = self.get_queryset()
        kwargs['destockages'] = self.get_destockages()
        kwargs['sales_flash'] = self.get_sales_flash()
        kwargs['news_arrivals'] = self.get_news_arrivals()
        kwargs['product_recommended'] = utils.get_recently_viewed(self.request)
        return super().get_context_data(*args, **kwargs)


promotion_detail = PromotionDetailView.as_view()


class CampaignMixinObject(mixins.PromotionMixin, generic.ListView):

    paginate_by = 20
    template_name = "pages/promotion/_list.html"

    def get_context_data(self, **kwargs):
        kwargs["query"] = self.request.GET.get("q", None)
        kwargs['promotion_list'] = self.get_promotions_list()
        kwargs['product_recommended'] = utils.get_recently_viewed(self.request)

        return super().get_context_data(**kwargs)


class ProductOnSaleFlashListView(CampaignMixinObject):
    extra_context = {'page_title': 'Ventes Flash'}
    queryset = models.Campaign.objects.ventes_flash()

    def get_context_data(self, **kwargs):
        kwargs["query"] = self.request.GET.get("q", None)
        kwargs['promotion_list'] = self.get_promotions_list()
        kwargs['product_recommended'] = utils.get_recently_viewed(self.request)

        kwargs['destockages'] = self.get_destockages()
        kwargs['news_arrivals'] = self.get_news_arrivals()

        return super().get_context_data(**kwargs)


sales_flash_list_view = ProductOnSaleFlashListView.as_view()


class ProductOnDestockageListView(CampaignMixinObject):
    extra_context = {'page_title': 'Déstockages'}
    queryset = models.Campaign.objects.destockages()

    def get_context_data(self, **kwargs):
        kwargs["query"] = self.request.GET.get("q", None)
        kwargs['promotion_list'] = self.get_promotions_list()
        kwargs['product_recommended'] = utils.get_recently_viewed(self.request)

        kwargs['sales_flash'] = self.get_sales_flash()
        kwargs['news_arrivals'] = self.get_news_arrivals()

        return super().get_context_data(**kwargs)


destockage_list_view = ProductOnDestockageListView.as_view()


class ProductOnDNewsArrivalListView(CampaignMixinObject):
    extra_context = {'page_title': 'Nouveautés'}
    queryset = models.Campaign.objects.nouvelle_arrivages()

    def get_context_data(self, **kwargs):
        kwargs["query"] = self.request.GET.get("q", None)
        kwargs['promotion_list'] = self.get_promotions_list()
        kwargs['product_recommended'] = utils.get_recently_viewed(self.request)

        kwargs['destockages'] = self.get_destockages()
        kwargs['sales_flash'] = self.get_sales_flash()

        return super().get_context_data(**kwargs)


news_arrivals_list_view = ProductOnDNewsArrivalListView.as_view()
