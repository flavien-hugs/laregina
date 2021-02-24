# accounts/forms.py

from django import forms
from django.db import transaction
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from accounts.models import Customer

from crispy_forms import bootstrap, layout
from crispy_forms.helper import FormHelper
from allauth.account.forms import SignupForm, LoginForm

from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget

from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget

User = get_user_model()


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
                layout.Submit(
                    'submit',
                    'Se connecter',
                    css_class='mt-4 ps-btn btn-block text-uppercase border-0'
                ),
            ),
        )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        email_base, provider = email.split("@")
        domain, extension = provider.split('.')
        return email

    def form_valid(self, form):
        user = form.save()
        if self.request.user.is_authenticated:
            if self.request.user.is_buyer:
                login(self.request, user)
            return redirect('catalogue:product_list')


class MarketSignupForm(UserCreationForm):
    civility = forms.TypedChoiceField(
        label="Civilité", choices=User.CIVILITY_CHOICES,
        initial='1', coerce=str, required=True,
    )
    shipping_first_name = forms.CharField(label='Nom', max_length=120,
        widget=forms.TextInput(attrs={'placeholder': 'Entrez votre nom'}))
    shipping_last_name = forms.CharField(label='Prénom', max_length=120,
        widget=forms.TextInput(attrs={'placeholder': 'Entrez votre prénom'}))
    store = forms.CharField(label='Nom de votre Magasin', max_length=254, required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = 'signup_form_ajax'
        self.helper.form_class = 'signup_form_ajax'
        self.helper.form_method = 'POST'

        self.helper.layout = layout.Layout(
            layout.Row(
                layout.Column('civility', css_class='form-group col-md-2 mb-0'),
                layout.Column('shipping_first_name', css_class='form-group col-md-5 mb-0'),
                layout.Column('shipping_last_name', css_class='form-group col-md-5 mb-0'),
                css_class='form-row'
            ),

            layout.Row(
                layout.Column(
                    bootstrap.PrependedText(
                        'email', '',
                        placeholder='Entrez votre adresse email',
                    ),
                    css_class='form-group col-md-6 mb-0'
                ),

                layout.Column(
                    bootstrap.PrependedText(
                        'store', '', 
                        placeholder='Entrez le nom du votre magasin',
                    ),
                    css_class='form-group col-md-6 mb-0'
                ),
            ),

            bootstrap.Field(
                'password1', '',
                placeholder="Entrez votre mot de passe"
            ),

            bootstrap.Field(
                'password2', '',
                placeholder="Confirmez le mot de passe"
            ),

            bootstrap.FormActions(
                layout.Submit(
                    'submit', 'Créer mon compte',
                    css_class='mt-4 ps-btn btn-block text-uppercase border-0'
                )
            ),
        )

    class Meta:
        model = User
        fields = [
            'email', 'civility',
            'shipping_first_name', 
            'shipping_last_name',
            'store',
        ]

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        email_base, provider = email.split("@")
        domain, extension = provider.split('.')
        return cleaned_data

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_seller = True
        if commit:
            user.save()
        return user


class CustomerSignUpForm(forms.ModelForm):

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)

        self.helper.layout = layout.Layout(
            bootstrap.PrependedText('email', '', placeholder="Entrez votre adresse email"),
            bootstrap.FormActions(
                layout.Submit(
                    'submit', 'Créer mon compte',
                    css_class='mt-4 ps-btn btn-block text-uppercase border-0'
                ),
            ),
        )

    class Meta:
        model = Customer
        fields = ['email',]

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        email_base, provider = email.split("@")
        domain, extension = provider.split('.')
        return cleaned_data

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            self.request.session['customer_email_id'] = user.id
        return user


class MarketChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = [
            'civility',
            'shipping_first_name', 
            'shipping_last_name',
            'store', 'phone'
        ]


class StoreUpdateForm(forms.ModelForm):
    
    shipping_country = CountryField(blank_label='Sélection un pays').formfield(
        widget=CountrySelectWidget(attrs={
        'class': 'form-control custom-select'
    }))

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
            layout.Row(
                layout.Column('civility', css_class='form-group col-md-2 mb-0'),
                layout.Column('shipping_first_name', css_class='form-group col-md-5 mb-0'),
                layout.Column('shipping_last_name', css_class='form-group col-md-5 mb-0'),
                css_class='form-row'
            ),

            layout.Row(
                layout.Column('store',  css_class='form-group col-md-4 mb-0'),
                layout.Column('phone', css_class='form-group col-md-4 mb-0'),
                layout.Column('phone_two', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),

            layout.Row(
                layout.Column('shipping_country', css_class='form-group col-md-4 mb-0'),
                layout.Column('shipping_city', css_class='form-group col-md-4 mb-0'),
                layout.Column('shipping_adress', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),

            layout.Row(
                layout.Column('store_description', css_class='form-group col-md-12 mb-0'),
            ),

            layout.Row(
                layout.Column('facebook', css_class='form-group col-md-6 mb-0'),
                layout.Column('instagramm', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),

            layout.Row(
                layout.Column('twitter', css_class='form-group col-md-6 mb-0'),
                layout.Column('linkedin', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),

            bootstrap.FormActions(
                layout.Submit(
                    'submit',
                    'Mettre à jour',
                    css_class='mt-4 ps-btn btn-block text-uppercase border-0'
                ),
            ),
        )

    class Meta:
        model = User
        fields = [
            "civility",
            "shipping_first_name",
            "shipping_last_name",
            "store",
            "phone",
            "phone_two",
            "shipping_country",
            "shipping_city",
            "store_description",
            "shipping_adress",
            "facebook",
            "twitter",
            "linkedin",
            "instagramm"
        ]
