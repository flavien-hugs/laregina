# accounts/forms.py

from django import forms


from crispy_forms import bootstrap, layout
from crispy_forms.helper import FormHelper
from accounts.models import UserProfile, StoreProfile
from allauth.account.forms import SignupForm, LoginForm


from django_countries.fields import CountryField
from phonenumber_field.formfields import PhoneNumberField


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
    type = forms.ChoiceField(label='Type d\'utilisateur', choices=UserProfile.ACCOUNT_TYPE_CHOICES)
    name = forms.CharField(label='Nom de la boutique', max_length=200)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)

        self.helper.layout = layout.Layout(
            layout.Fieldset(
                'Créer votre compte en quelques secondes.',
                bootstrap.PrependedText('email', '', placeholder="Entrez votre adresse email"),
                bootstrap.PrependedText('name', '', placeholder="Entrez le nom de votre boutique"),
                'type',
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
                'phone_number',
                'country',
                'tagline',
                'store_description',
            ),
            bootstrap.FormActions(
                layout.Submit('submit', 'Update profile', css_class='btn btn-success'),
            )
        )


class UserProfileForm(forms.Form):
    # Ce formulaire est utilisé lors de l'inscription pour créer automatiquement les objets UserProfile et StoreProfile
    # Notez que ce n'est PAS le formulaire effectivement vu par l'utilisateur

    def signup(self, request, user):
        # Créer automatiquement un profil d'utilisateur pour chaque utilisateur
        profile = UserProfile.objects.create(user=user, type=self.cleaned_data['type'], name=self.cleaned_data['name'])

        # Créer un profil vide si l'utilisateur est un vendeur
        if profile.is_seller:
            StoreProfile.objects.create(owner=profile)