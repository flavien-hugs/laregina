# catalogue.forms.py

from django import forms
from django.forms.models import inlineformset_factory

from catalogue.models import Product, ProductImage
from django_summernote.widgets import SummernoteWidget


class ProductAdminForm(forms.ModelForm):

    class Meta:
        model = Product
        exclude = ('user', 'quantity', 'slug', 'updated_at', 'created_at', 'timestamp')

        widgets = {'description': SummernoteWidget()}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

            if self.fields['price']:
                self.fields['price'].widget.attrs.update({'type': 'text'})

        self.fields['is_external'].widget.attrs['type'] = 'checkbox'
        self.fields['name'].widget.attrs['placeholder'] = 'Entrer le nom du produit'
        self.fields['price'].widget.attrs['placeholder'] = 'Entrer le prix de vente du produit'
        self.fields['keywords'].widget.attrs['placeholder'] = 'Ajouter quelques mots-clés (facultatif)'

    def clean(self):
        cleaned_data = super().clean()
        price = cleaned_data.get('price')

        if price <= 100:
            msg = "Le prix doit être supérieur à 100 Fr !"
            self.errors['price'] = self.error_class([msg])
        return cleaned_data


class ProductImageForm(forms.ModelForm):

    image = forms.ImageField(label="Ajouter des images", required=True)

    class Meta:
        model = ProductImage
        fields = ('image',)


ProductCreateFormSet = inlineformset_factory(
    Product, ProductImage,
    fields=[
        'product',
        'image'
    ],
    exclude=[
        'timestamp',
        'updated',
    ],
    can_delete=False,
    extra=4
)

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
