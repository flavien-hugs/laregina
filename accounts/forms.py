from accounts import models
from crispy_forms import bootstrap
from crispy_forms import layout
from crispy_forms.helper import FormHelper
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.forms.widgets import NumberInput
from helpers.utils import email_validation_function


class AccountMixinForm:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update(
                {"class": "form-control shadow-none"}
            )


class AccountLoginForm(AccountMixinForm, forms.Form):
    required_css_class = "required"

    email = forms.EmailField(
        label="Adresse email",
        widget=forms.TextInput({"placeholder": "Entrez votre adresse email"}),
    )
    password = forms.CharField(
        label="Mot de passe",
        widget=forms.PasswordInput({"placeholder": "Entrez votre mot de passe"}),
    )


class AccountRegisterForm(AccountMixinForm, UserCreationForm):
    required_css_class = "required"

    error_message = UserCreationForm.error_messages.update(
        {"duplicate_email": "Cette adresse est déjà utilisé par un autre utilisateur."}
    )
    email = forms.EmailField(
        label="Adresse email",
        widget=forms.TextInput({"placeholder": "Entrez votre adresse email"}),
    )
    phone = forms.CharField(
        label="Téléphone",
        widget=forms.TextInput(
            {"placeholder": "Téléphone avec indicatif de votre pays, Ex: +225xxxxx"}
        ),
    )
    password1 = forms.CharField(
        label="Mot de passe",
        widget=forms.PasswordInput({"placeholder": "Entrez votre mot de passe"}),
    )
    password2 = forms.CharField(
        label="Confirmation Mot de passe",
        widget=forms.PasswordInput({"placeholder": "Confirmez le mot de passe"}),
    )

    class Meta:
        model = get_user_model()
        fields = ["email", "phone", "password1", "password2"]

    def clean_email(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        if email_validation_function(email):
            return email

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_customer = True
        if commit:
            user.save()
        return user


class AccountRequestPasswordResetForm(AccountMixinForm, forms.Form):
    required_css_class = "required"

    email = forms.EmailField(
        label="Adresse email",
        widget=forms.TextInput({"placeholder": "Entrez votre adresse email"}),
    )


class AccountUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)

        self.helper.layout = layout.Layout(
            layout.Row(
                layout.Column("gender", css_class="col-md-2"),
                layout.Column("firstname", css_class="col-md-10"),
                css_class="row mb-4",
            ),
            layout.Row(
                layout.Column("lastname", css_class="col-md-12"),
                css_class="row mb-4",
            ),
            layout.Row(
                layout.Column("avatar", css_class="col-md-12 mb-3"),
            ),
            layout.Row(
                layout.Column("phone", css_class="col-md-6"),
                layout.Column("phone_two", css_class="col-md-6"),
                css_class="row mb-4",
            ),
            layout.Row(
                layout.Column("country", css_class="col-md-6"),
                layout.Column("city", css_class="col-md-6"),
                css_class="row mb-4",
            ),
            layout.Row(
                layout.Column("description", css_class="col-md-12 mb-3"),
            ),
            bootstrap.FormActions(
                layout.Submit(
                    "submit",
                    "mettre à jour votre compte",
                    css_class="btn btn-secondary text-uppercase rounded-0",
                ),
            ),
        )

        for field in self.fields:
            self.fields[field].widget.attrs[
                "class"
            ] = "form-control shadow-none rounded-0"

    class Meta:
        model = get_user_model()
        fields = [
            "gender",
            "firstname",
            "lastname",
            "phone",
            "phone_two",
            "country",
            "city",
            "description",
            "avatar",
        ]


class MarketChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = [
            "gender",
            "firstname",
            "lastname",
            "phone",
        ]


class DistributorCustomerForm(AccountMixinForm, forms.ModelForm):
    privacy = forms.BooleanField(
        label="Conditions légales d'utilisation des données",
        initial=True,
        required=True,
    )
    birth_date = forms.DateField(
        label="Date de naisssance", widget=NumberInput(attrs={"type": "date"})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        fields = ["gender", "marital_status", "level_of_education"]
        for field in fields:
            if (
                self.fields["gender"]
                and self.fields["marital_status"]
                and self.fields["level_of_education"]
            ):
                self.fields[field].widget.attrs.update(
                    {"class": "form-control custom-select"}
                )

        self.fields["phone"].widget.attrs["placeholder"] = "Ex: +225xxxxxxxxx"
        self.fields["phone_two"].widget.attrs["placeholder"] = "Ex: +225xxxxxxxxx"
        self.fields["shipping_city"].widget.attrs["placeholder"] = "Ville de résidence"

    class Meta:
        model = models.DistributorCustomer
        fields = "__all__"
        exclude = ["active", "created_at", "updated_at"]
        labels = {
            "profession": "Quelle activité vous exercez actuellement ?",
            "commune": "Vous habitez dans quelle commune ?",
            "district": "Veuillez préciser le nom de votre quartier",
            "local_market": "Quel est le marché le plus proche de chez vous ?",
            "privacy": "En validant votre inscription, vous acceptez toutes les Conditions d'Utilisations de vos données transmises.",
        }

    def validate_birth_date(self):
        birth_date = self.cleaned_data["birth_date"].year
        return 1992 <= birth_date < 2004
