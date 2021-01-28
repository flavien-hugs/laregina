# catalogue.forms.py

from django import forms
from django.forms.models import modelformset_factory

from category.models import Category
from catalogue.models import Product, Variation


class ProductAdminForm(forms.ModelForm):

    class Meta:
        model = Variation
        exclude = ('updated_at', 'created_at', 'timestamp')
        
    def clean_price(self):
        if self.cleaned_data['price'] <= 0:
            raise forms.ValidationError('Le prix fourni doit être supérieur à zéro.')
        return self.cleaned_data['price']

    def clean_product_name(self):
        value = self.cleaned_data.get('name')
        if len(value.strip()) < 5 :
            raise ValidationError("Le nom du produit doit être long de 4 caractères....")
        return value.strip()


class ProductAddToCartForm(forms.Form):
    """ 
    classe de formulaire pour
    ajouter des articles au panier
    """

    quantity = forms.IntegerField(
        widget=forms.TextInput(
            attrs={
                'type': 'hidden',
                'value': '1',
                'class': 'form-control'
            }),
            error_messages={
                'invalid':' Veuillez entrer une quantité valide.'
            },
            min_value=1
        )
    slug = forms.CharField(widget=forms.HiddenInput())
    
    def __init__(self, request=None, *args, **kwargs):
        """
        passer outre la valeur par défaut afin que
        nous puissions définir la demande
        """
        self.request = request
        super(ProductAddToCartForm, self).__init__(*args, **kwargs)
    
    def clean(self):
        """ 
        validation personnalisée pour vérifier
        la présence de cookies dans le navigateur du client
        """
        if self.request:
            if not self.request.session.test_cookie_worked():
                raise forms.ValidationError("Les cookies doivent être activés.")
        return self.cleaned_data


class VariationInventoryForm(forms.ModelForm):
    class Meta:
        model = Variation
        fields = [
            "price",
            "sale_price",
            "inventory",
            "is_active",
        ]

VariationInventoryFormSet = modelformset_factory(Variation, form=VariationInventoryForm, extra=0)


# class ProductReviewForm(forms.ModelForm):
#     Form class to submit a new ProductReview instance 
#     class Meta:
#         model = ProductReview
#         exclude = ('user','product', 'is_approved')
        
