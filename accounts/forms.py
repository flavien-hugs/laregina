# accounts/forms.py

from django import forms
from django.db import transaction
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from crispy_forms import bootstrap, layout
from crispy_forms.helper import FormHelper
from allauth.account.forms import SignupForm, LoginForm

from django_countries.fields import CountryField
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget

# User Manager
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
        if user.is_buyer:
            login(self.request, user)
            return redirect('list')


class MarketSignupForm(UserCreationForm):
    civility = forms.TypedChoiceField(
        label="Civilité", choices=User.CIVILITY_CHOICES,
        initial = '1', coerce=str, required = True,
    )
    shipping_first_name = forms.CharField(label='Nom', max_length=120,
        widget=forms.TextInput(attrs={'placeholder': 'Entrez votre nom'}))
    shipping_last_name = forms.CharField(label='Prénom', max_length=120,
        widget=forms.TextInput(attrs={'placeholder': 'Entrez votre prénom'}))
    phone = PhoneNumberField(label='Numéro de téléphone', region='IT', initial='+39',
        widget=PhoneNumberPrefixWidget(
            attrs={'placeholder': 'ex.: 015 157 139 6000',
            'class': "form-control"}
        )
    )
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

            bootstrap.PrependedText(
                'email', '',
                placeholder='Entrez votre adresse email',
                css_class='form-group'
            ),
            
            bootstrap.PrependedText(
                'store', '', 
                placeholder='Entrez le nom du votre magasin',
                css_class='form-group'
            ),

            bootstrap.PrependedText(
                'phone', '', css_class='form-group custom-select'
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
            'store', 'phone'
        ]

    def clean_email(self):
        email = self.cleaned_data.get('email')
        email_base, provider = email.split("@")
        domain, extension = provider.split('.')
        return email

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
    
    shipping_first_name = forms.CharField(label='Nom', max_length=120,
        widget=forms.TextInput(
            attrs={'placeholder': 'Entrez votre nom'}
        )
    )

    shipping_last_name = forms.CharField(label='Prénoms', max_length=120,
        widget=forms.TextInput(
            attrs={'placeholder': 'Entrez votre prénom'}
        )
    )

    phone = PhoneNumberField(
        label='Numéro de téléphone', initial='+39',
        widget=PhoneNumberPrefixWidget(
            attrs={'placeholder': '000 000 0000', 'class': "form-control"}
        )
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
            bootstrap.PrependedText('email', '', placeholder="Entrez votre adresse email"),
            bootstrap.PrependedText('phone', '', css_class='custom-select'),
            bootstrap.PrependedText('password1', '', placeholder="Entrez votre mot de passe"),
            bootstrap.PrependedText('password2', '', placeholder="Confirmez le mot de passe"),

            bootstrap.FormActions(
                layout.Submit(
                    'submit', 'Créer mon compte',
                    css_class='mt-4 ps-btn btn-block text-uppercase border-0'
                ),
            ),
        )

    class Meta:
        model = User
        fields = (
            'email', 'civility',
            'shipping_first_name', 'shipping_last_name',
            'phone'
        )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        email_base, provider = email.split("@")
        domain, extension = provider.split('.')
        return email

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_buyer = True
        if commit:
            user.save()
        return user


class MarketChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ("email", "logo")



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
            layout.Row(
                layout.Column('civility', css_class='form-group col-md-2 mb-0'),
                layout.Column('shipping_first_name', css_class='form-group col-md-5 mb-0'),
                layout.Column('shipping_last_name', css_class='form-group col-md-5 mb-0'),
                css_class='form-row'
            ),

            layout.Row(
                layout.Column('phone', css_class='form-group col-md-6 mb-0'),
                layout.Column('phone_two', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),

            layout.Row(
                layout.Column('store', css_class='form-group col-md-6 mb-0'),
                layout.Column('logo', css_class='form-group col-md-6 mb-0'),
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
            "logo",
            "phone",
            "phone_two",
            "shipping_country",
            "shipping_city",
            "store_description",
            "shipping_adress",
        ]
