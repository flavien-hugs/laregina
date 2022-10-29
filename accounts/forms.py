from django import forms
from django.db import transaction
from django.contrib.auth import get_user_model
from django.forms.models import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from accounts import models

from crispy_forms import bootstrap, layout
from crispy_forms.helper import FormHelper
from helpers.utils import email_validation_function
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget


class AccountMixinForm:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update(
                {'class': 'form-control form-control-md shadow-none'}
            )


class AccountLoginForm(AccountMixinForm, forms.Form):

    required_css_class = 'required'

    email = forms.EmailField(
        label="Adresse email",
        widget=forms.TextInput(
            {"placeholder": "Entrez votre adresse email"}
        )
    )
    password = forms.CharField(
        label="Mot de passe",
        widget=forms.PasswordInput(
            {"placeholder": "Entrez votre mot de passe" }
        )
    )

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_method = 'post'

        self.helper.layout = layout.Layout(
            layout.Field('email'),
            bootstrap.Field('password'),
            bootstrap.FormActions(
                layout.Submit(
                    'submit',
                    'Se connecter',
                    css_class='mt-4 ps-btn btn-block text-uppercase border-0'
                ),
            ),
        )


class AccountSellerRegisterForm(AccountMixinForm, UserCreationForm):

    required_css_class = 'required'

    error_message = UserCreationForm.error_messages.update(
        {
            "duplicate_email": "Cette adresse est déjà utilisé par un autre utilisateur."
        }
    )

    store = forms.CharField(
        label='Nom de votre Magasin',
        max_length=254, required=True,
        widget=forms.TextInput(
            {"placeholder": "Entrez le nom du votre magasin"}
        )
    )
    shipping_city = forms.CharField(
        label='Ville',
        max_length=254, required=True,
        widget=forms.TextInput(
            {"placeholder": "Situation du magasin"}
        )
    )
    email = forms.EmailField(
        label="Adresse email",
        widget=forms.TextInput(
            {"placeholder": "Entrez votre adresse email"}
        )
    )
    phone = forms.CharField(
        label="Téléphone",
        widget=forms.TextInput(
            {"placeholder": "Téléphone avec indicatif de votre pays, Ex: +225xxxxx"}
        )
    )
    password1 = forms.CharField(
        label="Mot de passe",
        widget=forms.PasswordInput(
            {"placeholder": "Entrez votre mot de passe"}
        ),
    )
    password2 = forms.CharField(
        label="Confirmation Mot de passe",
        widget=forms.PasswordInput(
            {"placeholder": "Confirmez le mot de passe"}
        ),
    )

    class Meta:
        model = get_user_model()
        fields = [
            'email', 'shipping_country',
            'shipping_city', 'phone', 'store'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update(
                {'class': 'form-control'}
            )

        self.helper = FormHelper(self)
        self.helper.form_method = 'post'

        self.helper.layout = layout.Layout(
            layout.Row(
                layout.Column(
                    'email',
                    css_class='form-group col-md-6 mb-0'
                ),

                layout.Column(
                    'store',
                    css_class='form-group col-md-6 mb-0'
                ),
            ),
            layout.Row(
                layout.Column(
                    'shipping_country',
                    css_class='form-group col-md-6 mb-0'
                ),
                layout.Column(
                    'shipping_city',
                    css_class='form-group col-md-6 mb-0'
                ),
            ),
            layout.Field('phone'),
            bootstrap.Field('password1'),
            bootstrap.Field('password2'),

            bootstrap.FormActions(
                layout.Submit(
                    'submit', 'Créer mon compte',
                    css_class='mt-4 ps-btn btn-block text-uppercase border-0'
                )
            ),
        )

    def clean_email(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        if email_validation_function(email):
            return email

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_seller = True
        if commit:
            user.save()
        return user


class AccountRequestPasswordResetForm(AccountMixinForm, forms.Form):

    required_css_class = 'required'

    email = forms.EmailField(
        label="Adresse email",
        widget=forms.TextInput(
            {"placeholder": "Entrez votre adresse email"}
        )
    )

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_method = 'post'

        self.helper.layout = layout.Layout(
            layout.Field('email'),
            bootstrap.FormActions(
                layout.Submit(
                    'submit',
                    'obtenir un lien de réinitialisationr',
                    css_class='mt-4 ps-btn btn-block text-uppercase border-0'
                ),
            ),
        )


class AccountSellerUpdateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)

        self.helper.layout = layout.Layout(
            layout.Row(
                layout.Column('civility', css_class='col-md-2'),
                layout.Column('shipping_first_name', css_class='col-md-10'),
                css_class='row mb-4'
            ),

            layout.Row(
                layout.Column('shipping_last_name', css_class='col-md-12'),
                css_class='row mb-4'
            ),

            layout.Row(
                layout.Column('logo', css_class='col-md-12 mb-3'),
            ),

            layout.Row(
                layout.Column('store', css_class='col-md-6'),
                layout.Column('phone', css_class='col-md-6'),
                css_class='row mb-4'
            ),

            layout.Row(
                layout.Column('phone_two', css_class='col-md-12'),
                css_class='row mb-4'
            ),

            layout.Row(
                layout.Column('shipping_country', css_class='col-md-6'),
                layout.Column('shipping_city', css_class='col-md-6'),
                css_class='row mb-4'
            ),

            layout.Row(
                layout.Column('shipping_adress', css_class='col-md-12'),
                css_class='row mb-4'
            ),

            layout.Row(
                layout.Column('store_description', css_class='col-md-12 mb-3'),
            ),

            bootstrap.FormActions(
                layout.Submit(
                    'submit',
                    'mettre à jour votre compte',
                    css_class='btn btn-secondary text-uppercase rounded-0'
                ),
            ),
        )

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control shadow-none rounded-0'

    class Meta:
        model = get_user_model()
        fields = [
            "civility", "shipping_first_name",
            "shipping_last_name", "store", "phone",
            "phone_two", "shipping_country",
            "shipping_city", "store_description",
            "shipping_adress", "logo",
        ]


class CustomInlineFormSet(AccountMixinForm, forms.ModelForm):
    class Meta:
        model = models.ProfileSocialMedia
        fields = [
            "facebook",
            "instagram"
        ]

    def __init__(self, *args, **kwargs):
        super(CustomInlineFormSet, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update(
                {'class': 'shadow-none rounded-0 mb-2'}
            )


SocialMediaForm = inlineformset_factory(
    get_user_model(), models.ProfileSocialMedia,
    fk_name='user', form=CustomInlineFormSet,
    fields=['facebook', 'instagram'],
    can_delete=False, extra=1, max_num=1
)


# -------------------------------------------------
# -------------- CUSTOMER ACCOUNT FORMS -----------
# -------------------------------------------------

class CustomerAccountSignUpForm(forms.ModelForm):

    email = forms.EmailField(
        label="Adresse email",
        widget=forms.TextInput(
            {"placeholder": "Entrez votre adresse email"}
        )
    )
    phone = forms.CharField(
        label="Téléphone",
        widget=forms.TextInput(
            {"placeholder": "Téléphone avec indicatif de votre pays, Ex: +225xxxxx"}
        )
    )
    password1 = forms.CharField(
        label="Mot de passe",
        widget=forms.PasswordInput(
            {"placeholder": "Entrez votre mot de passe"}
        ),
    )
    password2 = forms.CharField(
        label="Confirmation Mot de passe",
        widget=forms.PasswordInput(
            {"placeholder": "Confirmez le mot de passe"}
        ),
    )

    class Meta:
        model = models.GuestCustomer
        fields = ['email']

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update(
                {'class': 'form-control'}
            )

        self.helper = FormHelper(self)
        self.helper.form_method = 'post'

        self.helper.layout = layout.Layout(
            layout.Row(
                layout.Column(
                    'email',
                    css_class='form-group col-md-6 mb-0'
                ),

                layout.Column(
                    'phone',
                    css_class='form-group col-md-6 mb-0'
                ),
            ),
            bootstrap.Field('password1'),
            bootstrap.Field('password2'),

            bootstrap.FormActions(
                layout.Submit(
                    'submit', 'Créer mon compte',
                    css_class='mt-4 ps-btn btn-block text-uppercase border-0'
                )
            ),
        )

    def clean_email(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        if validate_email(email):
            return email

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user


class MarketChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = [
            'civility',
            'shipping_first_name',
            'shipping_last_name',
            'store', 'phone'
        ]
