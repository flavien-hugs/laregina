# checkout.forms.py

from django import forms
from checkout.models import Order


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

            if self.fields['shipping_country']:
                self.fields['shipping_country'].widget.attrs.update({'class': 'form-control custom-select'})

        note_placehoder = "Commentaires concernant votre commande, ex.: consignes de livraison."
        shipping_adress_text = 'Votre adresse géographique, ex. : Quartier N°/Nom de la rue, etc.'

        self.fields['email'].widget.attrs['placeholder'] = 'Entrer votre adresse email'
        self.fields['shipping_last_name'].widget.attrs['placeholder'] = 'Entrer votre prénom'
        self.fields['shipping_first_name'].widget.attrs['placeholder'] = 'Entrer votre nom'
        self.fields['phone'].widget.attrs['placeholder'] = 'Numéro de téléphone'
        self.fields['phone_two'].widget.attrs['placeholder'] = 'Numéro téléphone supplémentaire'
        self.fields['shipping_city'].widget.attrs['placeholder'] = 'Ville de résidence'
        self.fields['shipping_adress'].widget.attrs['placeholder'] = shipping_adress_text
        self.fields['shipping_zip'].widget.attrs['placeholder'] = 'Code postal'
        self.fields['emailing'].widget.attrs['type'] = 'checkbox'
        self.fields['note'].widget.attrs['rows'] = '5'
        self.fields['note'].widget.attrs['placeholder'] = note_placehoder


    class Meta:
        model = Order
        fields = '__all__'
        exclude = [
            'user',
            'status',
            'transaction_id',
            'ip_address',
        ]
