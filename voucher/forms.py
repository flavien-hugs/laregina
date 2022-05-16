# voucher.forms.py

from django import forms

from voucher.models import Voucher
from catalogue.models import Product


class VoucherCreateForm(forms.ModelForm):

    products = forms.ModelMultipleChoiceField(
        required=True,
        label="Choisir les produits",
        queryset=Product.objects.all(),
        widget=forms.SelectMultiple()
    )

    class Meta:
        model = Voucher
        fields = [
            "products",
            "discount",
            "is_active"
        ]
        localized_fields = [
            'created_at',
            'updated_at'
        ]

    def __init__(self, user, *args, **kwargs):
        super(VoucherCreateForm, self).__init__(*args, **kwargs)

        products = Product.objects.all().filter(user=user)
        vouchers = Voucher.objects.filter(user=user)
        product = [obj.pk for obj in vouchers]

        if 'product' in products:
            print(product)

        products_exists_in_voucher = products.exclude(voucher__in=product)

        self.fields['products'].queryset = products
        for field in self.fields:
            self.fields[field].widget.attrs.update(
                {'class': 'form-control shadow-none'}
            )

            if self.fields['is_active']:
                self.fields['is_active'].widget.attrs.update(
                    {'class': 'form-check-input shadow-none'}
                )

            if self.fields['products']:
                self.fields['products'].widget.attrs.update(
                    {'class': 'form-control shadow-none rounded-0 custom-select'}
                )
