# catalogue.forms.py

from django import forms
from django.forms.models import modelformset_factory

from category.models import Category
from catalogue.models import Product


class ProductAdminForm(forms.ModelForm):

    class Meta:
        model = Product
        exclude = ('user', 'quantity', 'slug', 'updated_at', 'created_at', 'timestamp')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

            if self.fields['price'] and self.fields['old_price']:
                self.fields['price'].widget.attrs.update({'type': 'text'})
                self.fields['old_price'].widget.attrs.update({'type': 'text'})

        self.fields['is_external'].widget.attrs['type'] = 'checkbox'
        self.fields['name'].widget.attrs['placeholder'] = 'Entrer le nom du produit'
        self.fields['price'].widget.attrs['placeholder'] = 'Entrer le prix de vente du produit'
        self.fields['old_price'].widget.attrs['placeholder'] = 'Entrer le prix normal du produit (facultatif)'
        self.fields['keywords'].widget.attrs['placeholder'] = 'Ajouter quelques mots-clés (facultatif)'

        
    def clean_price(self):
        price = self.fields['price']
        price = self.cleaned_data['price']
        if price <= 1.00:
            raise forms.ValidationError(
                'Le prix doit être supérieur à 1$'
            )
        return price

    def clean_product_name(self):
        name = self.fields['name']
        name = self.cleaned_data['name']
        if len(name.strip()) >= 4:
            return name.strip()
        else:
            raise ValidationError("Le nom du produit doit être long de 4 caractères....")
        

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
        super().__init__(*args, **kwargs)
    
    def clean(self):
        """ 
        validation personnalisée pour vérifier
        la présence de cookies dans le navigateur du client
        """
        if self.request:
            if not self.request.session.test_cookie_worked():
                raise forms.ValidationError("Les cookies doivent être activés.")
        return self.cleaned_data


class ProductInventoryForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            "price",
            "old_price",
            "is_active",
        ]

ProductInventoryFormSet = modelformset_factory(Product, form=ProductInventoryForm, extra=0)
