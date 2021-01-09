# accounts/forms.py

from django import forms
from django.db import transaction
from django.forms.utils import ValidationError
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from crispy_forms import bootstrap, layout
from crispy_forms.helper import FormHelper
from allauth.account.forms import SignupForm, LoginForm

from django_countries.fields import CountryField
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget

from accounts.models import Subject, User


class MarketLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = self.request.user
        self.helper = FormHelper(self)
        
        self.helper.layout = layout.Layout(
            layout.Fieldset(
                'Veuillez saisir votre adresse email et mot de passe pour vous connecter.',
                bootstrap.PrependedText('login', '', placeholder="Entrez votre adresse email"),
                bootstrap.PrependedText('password', '', placeholder="Entrez votre mot de passe"),
            ),

            bootstrap.FormActions(
                layout.Submit('submit', 'Se connecter', css_class='mt-4 ps-btn btn-block text-uppercase border-0'),
            ),
        )

    def form_valid(self, form):
        user = form.save()
        if user.is_buyer:
            login(self.request, user)
            return redirect('list')


class MarketSignupForm(UserCreationForm):
    gender = forms.ChoiceField(label="Sexe", choices=User.GENDER_CHOICES)
    name = forms.CharField(label='Nom & Prénoms', max_length=120)
    phone_number = PhoneNumberField(label='Numéro de téléphone', initial='+225',
        widget=PhoneNumberPrefixWidget(attrs={'placeholder': '00 00 00 00', 'class': "form-control"}))
    whatsapp_number = PhoneNumberField(label='Numéro de téléphone WhatsApp (optionel)', initial='+225', required=False,
        widget=PhoneNumberPrefixWidget(attrs={'placeholder': '00 00 00 00', 'class': "form-control"}))
    store = forms.CharField(label='Nom de votre Magasin', max_length=254, required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)

        self.helper.layout = layout.Layout(
            layout.Fieldset(
                'Inscrivez-vous et commencez à vendre dès aujourd\'hui - créez votre propre compte vendeur.',
                bootstrap.PrependedText('email', '', placeholder="Entrez le nom de votre Adresse e-mail"),
                bootstrap.PrependedText('gender', '', placeholder="choisir", css_class='custom-control'),
                bootstrap.PrependedText('name', '', placeholder="Entrez votre nom et prénoms"),
                bootstrap.PrependedText('store', '', placeholder="Entrez le nom de votre Magasin"),
                bootstrap.PrependedText('phone_number', '', placeholder=''),
                bootstrap.PrependedText('whatsapp_number', '', placeholder=''),
                bootstrap.PrependedText('password1', '', placeholder="Entrez votre mot de passe"),
                bootstrap.PrependedText('password2', '', placeholder="Confirmez le mot de passe"),
            ),

            bootstrap.FormActions(
                layout.Submit('submit', 'Créer mon compte', css_class='mt-4 ps-btn btn-block text-uppercase border-0'),
            ),
        )

    class Meta:
        model = User
        fields = ('email', 'gender', 'name', 'store', 'phone_number', 'whatsapp_number')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_seller = True
        if commit:
            user.save()
        return user


class MarketChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ("email", "logo")


class CustomerSignUpForm(UserCreationForm):
    interests = forms.ModelMultipleChoiceField(
        queryset=Subject.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)

        self.helper.layout = layout.Layout(
            layout.Fieldset(
                'Inscrivez-vous et commencez à acheter dès aujourd\'hui - créez votre propre compte acheteur.',
                bootstrap.PrependedText('email', '', placeholder="Entrez votre adresse email"),
                bootstrap.PrependedText('name', '', placeholder="Entrez votre nom complet"),
                bootstrap.PrependedText('password1', '', placeholder="Entrez votre mot de passe"),
                bootstrap.PrependedText('password2', '', placeholder="Confirmez le mot de passe"),
            ),

            layout.Fieldset(
                'Inscrivez-vous et commencez à acheter dès aujourd\'hui - créez votre propre compte acheteur.',
                'interests',
            ),

            bootstrap.FormActions(
                layout.Submit('submit', 'Créer mon compte', css_class='mt-4 ps-btn btn-block text-uppercase border-0'),
            ),
        )

    class Meta:
        model = User
        fields = ('email', 'name', 'interests')

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_buyer = True
        user.save()
        user.interests.add(*self.cleaned_data.get('interests'))
        return user


class CustomerInterestsForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('interests',)
        widgets = {
            'interests': forms.CheckboxSelectMultiple
        }


class StoreProfileUpdateForm(forms.ModelForm):

    logo = forms.FileField(
        label="Logo du Magasin",
        widget=forms.FileInput(
            {
                "class": "as-parent file-upload",
                "accept": "image/*",
            }
        ),
    )

    class Meta:
        model = User
        fields = [
            "name",
            "store",
            "logo",
            "phone_number",
            "whatsapp_number",
            "country",
            "city",
            "address",
            "facebook",
            "linkedin",
            "instagramm",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        
        self.helper.layout = layout.Layout(
            layout.Fieldset(
                '',
                "name",
                "store",
                "logo",
                "phone_number",
                "whatsapp_number",
                "country",
                "city",
                "address",
                "facebook",
                "linkedin",
                "instagramm"
            ),

            bootstrap.FormActions(
                layout.Submit('submit', 'Mettre à jour', css_class='mt-4 ps-btn btn-block text-uppercase border-0'),
            ),
        )
