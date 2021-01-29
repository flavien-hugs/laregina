# order.forms.py

from django import forms
from order.models import Order


class CheckoutForm(forms.ModelForm):
    
    """
    classe de formulaire de paiement
    pour recueillir les informations d'expédition
    de l'utilisateur pour passer une commande
    """

    def __init__(self, *args, **kwargs):
        super(CheckoutForm, self).__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

        self.fields['email'].widget.attrs['placeholder'] = 'Entrer votre adresse email'
        self.fields['phone'].widget.attrs['placeholder'] = 'Numéro de téléphone'
        self.fields['shipping_last_name'].widget.attrs['placeholder'] = 'Entrer votre prénom'
        self.fields['shipping_first_name'].widget.attrs['placeholder'] = 'Entrer votre nom'
        self.fields['shipping_address'].widget.attrs['placeholder'] = 'Numéro téléphone supplémentaire'
        self.fields['shipping_city'].widget.attrs['placeholder'] = 'Ville de résidence'
        self.fields['shipping_zip'].widget.attrs['placeholder'] = 'Code postal'
        self.fields['emailing'].widget.attrs['type'] = 'checkbox'


    class Meta:
        model = Order
        fields = '__all__'
        exclude = [
            'user',
            'status',
            'transaction_id',
            'ip_address',
        ]
