# order.forms.py

import re
import datetime
from django import forms
from order.models import Order


def cc_expire_years():

    """
    liste des années commençant avec la période actuelle
    de douze ans dans le futur
    """
    current_year = datetime.datetime.now().year
    years = range(current_year, current_year+12)
    return [(str(x),str(x)) for x in years]


def cc_expire_months():

    """
    liste des tuples contenant les mois de l'année
    à utiliser sous forme de carte de crédit.
    [('01','January'), ('02','February'), ... ]
    """

    months = []
    for month in range(1, 13):
        if len(str(month)) == 1:
            numeric = '0' + str(month)
        else:
            numeric = str(month)
        months.append((numeric, datetime.date(2009, month, 1).strftime('%B')))
    return months


CARD_TYPES = (
    ('Mastercard', 'Mastercard'),
    ('VISA', 'VISA'),
    ('Discover', 'Discover'),
)


def strip_non_numbers(data):
    """
    se débarrasse de tous les caractères non numériques
    """
    non_numbers = re.compile('\D')
    return non_numbers.sub('', data)


def cardLuhnChecksumIsValid(card_number):

    """
    vérifie que la carte passe une somme de contrôle Luhn mod-10 
    Taken from: http://code.activestate.com/recipes/172845/
    """

    sum = 0
    num_digits = len(card_number)
    oddeven = num_digits & 1
    for count in range(0, num_digits):
        digit = int(card_number[count])
        if not (( count & 1 ) ^ oddeven ):
            digit = digit * 2
        if digit > 9:
            digit = digit - 9
        sum = sum + digit
    return ( (sum % 10) == 0 )


class CheckoutForm(forms.ModelForm):
    
    """
    classe de formulaire de paiement
    pour recueillir les informations d'expédition
    de l'utilisateur pour passer une commande
    """

    credit_card_number = forms.CharField(
        label='Numéro carte de crédit',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Numéro carte de crédit'
            }),
            error_messages={'invalid': 'Le numéro de la carte de crédit est incorrect'},
        )

    credit_card_type = forms.TypedChoiceField(
        choices=CARD_TYPES,
        initial = '1',
        coerce=str,
    )

    credit_card_expire_month = forms.CharField(
        widget=forms.Select(choices=cc_expire_months())
    )

    credit_card_expire_year = forms.CharField(
        widget=forms.Select(choices=cc_expire_years())
    )

    credit_card_cvv = forms.CharField(label='CVV', required=False)

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

        self.fields['credit_card_cvv'].widget.attrs['placeholder'] = 'CVV'
        self.fields['credit_card_type'].widget.attrs['class'] = 'custom-select'


    class Meta:
        model = Order
        exclude = [
            'user',
            'status',
            'transaction_id',
            'ip_address',
        ]

    def clean_credit_card_number(self):

        """
        valider le numéro de la carte de crédit si elle
        est valide selon l'algorithme de Luhn
        """

        cc_number = self.cleaned_data['credit_card_number']
        stripped_cc_number = strip_non_numbers(cc_number)
        if not cardLuhnChecksumIsValid(stripped_cc_number):
            raise forms.ValidationError("La carte de crédit que vous avez saisie n'est pas valable.")

    # def clean_phone(self):
    #     phone = self.cleaned_data['phone']
    #     stripped_phone = strip_non_numbers(phone)
    #     if len(stripped_phone) < 10:
    #         raise forms.ValidationError(
    #             "Entrez un numéro de téléphone valide avec\
    #             l'indicatif régional (par exemple, 555-555-5555)"
    #         )
    #     return self.cleaned_data['phone']
