# catalogue.forms.py

from django import forms
from django.forms.models import inlineformset_factory

from category.models import Category
from catalogue.models import Product, ProductImage
from django_summernote.widgets import SummernoteWidget


class ProductAdminForm(forms.ModelForm):

    category = forms.ModelChoiceField(
        empty_label=None, required=True,
        label="Choisir une catégorie",
        queryset=Category.objects.all()
    )

    class Meta:
        model = Product
        exclude = ['user', 'quantity', 'slug', 'updated_at', 'is_external', 'created_at', 'timestamp']

        widgets = {'description': SummernoteWidget()}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control shadow-none rounded-0'

            if self.fields['is_active']:
                self.fields['is_active'].widget.attrs.update(
                    {'class': 'form-check-input shadow-none'}
                )

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
    Product, ProductImage, form=ProductImageForm,
    fields=[
        'product',
        'image'
    ],
    exclude=[
        'timestamp',
        'updated',
    ],
    can_delete=False, extra=4, max_num=4
)


class ProductAddToCartForm(forms.Form):

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
        self.request = request
        super().__init__(*args, **kwargs)
    
    def clean(self):
        if self.request:
            if not self.request.session.test_cookie_worked():
                raise forms.ValidationError("Les cookies doivent être activés.")
        return self.cleaned_data
