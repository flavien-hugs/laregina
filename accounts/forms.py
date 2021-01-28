# accounts/forms.py

from django import forms
from django.db import transaction
from django.contrib.auth import get_user_model
from django.forms.utils import ValidationError
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


from crispy_forms import bootstrap, layout
from crispy_forms.helper import FormHelper
from allauth.account.forms import SignupForm, LoginForm

from django_countries.fields import CountryField
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget

# User Manager
User = get_user_model()
from category.models import Category


class LoginForm(LoginForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = self.request.user
        self.helper = FormHelper(self)
        self.helper.form_id = 'login_form_ajax'
        self.helper.form_class = 'login_form_ajax form-group'
        self.helper.form_method = 'POST'
        
        self.helper.layout = layout.Layout(
            bootstrap.PrependedText('login', '', placeholder="Entrez votre adresse email"),
            bootstrap.PrependedText('password', '', placeholder="Entrez votre mot de passe"),

            bootstrap.FormActions(
                layout.Submit('submit', 'Se connecter', css_class='mt-4 ps-btn btn-block text-uppercase border-0'),
            ),
        )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        email_base, provider = email.split("@")
        domain, extension = provider.split('.')
        return email

    def form_valid(self, form):
        user = form.save()
        if user.is_buyer:
            login(self.request, user)
            return redirect('list')


class MarketSignupForm(UserCreationForm):
    civility = forms.TypedChoiceField(
        label="Civilité", choices=User.CIVILITY_CHOICES,
        initial = '1', coerce=str, required = True,
    )
    name = forms.CharField(label='Nom & Prénoms', max_length=120,
        widget=forms.TextInput(attrs={'placeholder': 'Entrez votre nom complet'}))
    phone_number = PhoneNumberField(label='Numéro de téléphone', initial='+225',
        widget=PhoneNumberPrefixWidget(attrs={'placeholder': '00 00 00 00', 'class': "form-control"}))
    store = forms.CharField(label='Nom de votre Magasin', max_length=254, required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = 'signup_form_ajax'
        self.helper.form_class = 'signup_form_ajax'
        self.helper.form_method = 'POST'

        self.helper.layout = layout.Layout(
            layout.Row(
                layout.Column('civility', css_class='form-group col-md-3 mb-0'),
                layout.Column('name', css_class='form-group col-md-9 mb-0'),
                css_class='form-row'
            ),

            bootstrap.PrependedText('email', '', placeholder='Entrez votre adresse email', css_class='form-group'),
            bootstrap.PrependedText('store', '', placeholder='Entrez le nom du votre magasin', css_class='form-group'),
            bootstrap.PrependedText('phone_number', '', css_class='form-group custom-select'),

            bootstrap.Field('password1', '', placeholder="Entrez votre mot de passe"),
            bootstrap.Field('password2', '', placeholder="Confirmez le mot de passe"),

            bootstrap.FormActions(
                layout.Submit('submit', 'Créer mon compte', css_class='mt-4 ps-btn btn-block text-uppercase border-0')
            ),
        )

    class Meta:
        model = User
        fields = ('email', 'civility', 'name', 'store', 'phone_number')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_seller = True
        if commit:
            user.save()
        return user


class CustomerSignUpForm(UserCreationForm):
    civility = forms.TypedChoiceField(
        label="Civilité", choices=User.CIVILITY_CHOICES,
        initial = '1', coerce=str, required = True,
    )
    name = forms.CharField(label='Nom & Prénoms', max_length=120,
        widget=forms.TextInput(attrs={'placeholder': 'Entrez votre nom complet'}))
    phone_number = PhoneNumberField(label='Numéro de téléphone', initial='+225',
        widget=PhoneNumberPrefixWidget(attrs={'placeholder': '00 00 00 00', 'class': "form-control"}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)

        self.helper.layout = layout.Layout(
            layout.Row(
                layout.Column('civility', css_class='form-group col-md-3 mb-0'),
                layout.Column('name', css_class='form-group col-md-9 mb-0'),
                css_class='form-row'
            ),
            bootstrap.PrependedText('email', '', placeholder="Entrez votre adresse email"),
            bootstrap.PrependedText('phone_number', '', css_class='custom-select'),
            bootstrap.PrependedText('password1', '', placeholder="Entrez votre mot de passe"),
            bootstrap.PrependedText('password2', '', placeholder="Confirmez le mot de passe"),

            bootstrap.FormActions(
                layout.Submit('submit', 'Créer mon compte', css_class='mt-4 ps-btn btn-block text-uppercase border-0'),
            ),
        )

    class Meta:
        model = User
        fields = ('email', 'civility', 'name', 'phone_number')

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_buyer = True
        if commit:
            user.save()
        return user


class MarketChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ("email", "logo")


@permission_required('user.is_seller', raise_exception=True)
class StoreUpdateForm(forms.ModelForm):

    logo = forms.FileField(
        label="Logo du Magasin",
        widget=forms.FileInput(
            {
                "class": "as-parent file-upload",
                "accept": "image/*",
            }
        ), required=False,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)

        self.helper.layout = layout.Layout(
            layout.Fieldset(
                '',
                "civility",
                "name",
                "store",
                "logo",
                "phone_number",
                "whatsapp_number",
                "country",
                "city",
                "store_description",
                "address",
                "facebook",
                "linkedin",
                "instagramm"
            ),

            bootstrap.FormActions(
                layout.Submit('submit', 'Mettre à jour', css_class='mt-4 ps-btn btn-block text-uppercase border-0'),
            ),
        )

    class Meta:
        model = User
        fields = [
            "civility",
            "name",
            "store",
            "logo",
            "phone_number",
            "whatsapp_number",
            "country",
            "city",
            "store_description",
            "address",
            "facebook",
            "linkedin",
            "instagramm",
        ]
