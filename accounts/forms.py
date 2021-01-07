# accounts/forms.py

from django import forms


from crispy_forms import bootstrap, layout
from crispy_forms.helper import FormHelper
from accounts.models import UserProfile, StoreProfile
from allauth.account.forms import SignupForm, LoginForm

from django_countries.fields import CountryField
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget


class MarketLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
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


class MarketSignupForm(SignupForm):
    name = forms.CharField(label='Nom de la boutique', max_length=200)
    type = forms.ChoiceField(label="Type d'utilisateur", choices=UserProfile.ACCOUNT_TYPE_CHOICES)
    phone_number = PhoneNumberField(label='Numéro de téléphone', initial='+225', widget=PhoneNumberPrefixWidget(
        attrs={'placeholder': '00 00 00 00', 'class': "form-control"}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)

        self.helper.layout = layout.Layout(
            layout.Fieldset(
                'Inscrivez-vous et commencez à vendre dès aujourd\'hui - créez votre propre compte vendeur.',
                bootstrap.PrependedText('email', '', placeholder="Entrez votre adresse email"),
                bootstrap.PrependedText('name', '', placeholder="Entrez le nom de votre magasin"),
                bootstrap.PrependedText('phone_number', '', placeholder="Numéro de téléphone", css_class='form-control'),
                bootstrap.PrependedText('type', '', placeholder="Type d'utilisateur", css_class='form-control'),
                bootstrap.PrependedText('password1', '', placeholder="Entrez votre mot de passe"),
                bootstrap.PrependedText('password2', '', placeholder="Confirmez le mot de passe"),
            ),

            bootstrap.FormActions(
                layout.Submit('submit', 'Créer mon compte', css_class='mt-4 ps-btn btn-block text-uppercase border-0'),
            ),
        )

    def signup(self, request, user):
        user.email = self.cleaned_data['email']
        user.save()
        return user


class StoreProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = StoreProfile
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.layout = layout.Layout(
            layout.Fieldset(
                '',
                'avatar',
                'country',
                'tagline',
                'store_description',
            ),
            bootstrap.FormActions(
                layout.Submit('submit', 'Update profile', css_class='mt-4 ps-btn btn-block text-uppercase border-0'),
            )
        )


class UserProfileForm(forms.ModelForm):
    # Ce formulaire est utilisé lors de l'inscription pour créer automatiquement les objets UserProfile et StoreProfile
    # Notez que ce n'est PAS le formulaire effectivement vu par l'utilisateur

    def signup(self, request, user):
        # Créer automatiquement un profil d'utilisateur pour chaque utilisateur
        profile = UserProfile.objects.create(user=user, type=self.cleaned_data['type'], name=self.cleaned_data['name'])

        # Créer un profil vide si l'utilisateur est un vendeur
        if profile.is_seller:
            StoreProfile.objects.create(owner=profile)