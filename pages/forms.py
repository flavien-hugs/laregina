# pages.forms.py

from django import forms
from pages.models import Contact



OBJECT_TYPES = (
    ('Choisissez le sujet', 'Choisissez le sujet'),
    ('Mon article est introuvable', 'Mon article est introuvable'),
    ('Je souhaite être un partenaire de LaRegina', 'Je souhaite être un partenaire de LaRegina'),
    ('Je souhaite annuler une commande', 'Je souhaite annuler une commande'),
    ('Je souhaite signaler une anarque', 'Je souhaite signaler une anarque'),
    ("J'ai un problème avec le paiement", "J'ai un problème avec le paiement"),
    ("J'ai d'autres demandes", "J'ai d'autres demandes"),
)


class ContactForm(forms.ModelForm):
    full_name = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            "placeholder": "Nom ex.: Flavien HUGS"
        }),
    )
    email = forms.EmailField(
        max_length=150,
        required=True,
        widget=forms.EmailInput(attrs={
            "placeholder": "Mail, ex.: monmail@gmail.com"
        }),
    )
    phone = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            "placeholder": "Tél. ex.: +225 77 27 28 48",
        }),
    )

    subject = forms.ChoiceField(
        required=True,
        choices=OBJECT_TYPES,
        widget=forms.Select(attrs={"class": "custom-select",}),
    )

    company = forms.CharField(
        max_length=150,
        required=False,
        widget=forms.TextInput(attrs={
            "placeholder": "Votre Magasin ou Entreprise (Optionnel)"
        }),
    )

    message = forms.CharField(
        required=True,
        widget=forms.Textarea(
            attrs={
                "rows": 5,
                "placeholder": "Votre message"
            }
        ),
    )

    class Meta:
        model = Contact
        fields = [
            "full_name",
            "company",
            "email",
            "phone",
            "subject",
            "message"
        ]

    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

            if self.fields['subject']:
                self.fields['subject'].widget.attrs.update({'class': 'form-control custom-select'})

    def clean_email(self):
        email = self.cleaned_data.get('email')
        email_base, provider = email.split("@")
        domain, extension = provider.split('.')
        return email

    def clean_full_name(self):
        value = self.cleaned_data.get('full_name')
        if len(value.strip()) < 4:
            raise ValidationError("Le Nom et prénoms doivent être supérieur à 4 lettre....")
        return value.strip()