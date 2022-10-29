from django.urls import reverse
from django.conf import settings
from django.views import generic

from django.contrib import messages
from django.urls import reverse_lazy
from django.core.mail import EmailMessage
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError


from helpers.utils import EmailThread
from validate_email import validate_email
from accounts.forms import(
    AccountSellerRegisterForm, AccountLoginForm, AccountRequestPasswordResetForm
)


def sellerSignupView(request, template='account/signup.html'):

    form = AccountSellerRegisterForm()
    if request.method == 'POST':
        form = AccountSellerRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f"Compte crée avec succès. Veuillez vous connecter à votre tableau de bord !")
            return redirect(reverse(settings.LOGIN_REDIRECT_URL))
        messages.error(request, "Veuillez vérifier les informations fournies !")
    context = {
        "form": form,
        "page_title": "Créer votre boutique"
    }
    return render(request, template, context)


seller_signup_view = sellerSignupView


class AccountLoginView(generic.View):

    form_class = AccountLoginForm
    template_name = 'account/login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(
                reverse_lazy(settings.LOGIN_REDIRECT_URL)
            )
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class()
        page_title = "Connexion"
        ctx = {'form': form, 'page_title': page_title}
        return render(request, self.template_name, ctx)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = authenticate(
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )
            print(user)
            if user is not None:
                login(request, user)
                messages.success(request, f"Vous êtes connecté en tant que {user.email}")
                return redirect(reverse(settings.LOGIN_REDIRECT_URL))
        messages.error(request, "Identifiants invalides ou compte désactivé !")

        page_title = "Connexion"
        context = {'form': form, 'page_title': page_title}
        return render(request, self.template_name, context)


user_login_view = AccountLoginView.as_view()


class AccountRequestPasswordResetView(generic.View):

    form_class  = AccountRequestPasswordResetForm
    template_name = 'account/password_reset.html'

    def get(self, request):
        form = self.form_class()
        page_title = "Réinitialisation du mot de passe"
        ctx = {'form': form, 'page_title': "Aide avec le mot de passe"}
        return render(request, self.template_name, ctx)

    def post(self, request):

        form = self.form_class(request.POST)

        email = request.POST.get('email', None)
        email_lower = email.lower()

        if not validate_email(email_lower):
            messages.error(request, 'Veuillez entrer une adresse email valide.')
            return render(request, self.template_name)

        if get_user_model().objects.filter(email=email_lower).exists():

            user = get_user_model().objects.get(email=email_lower)
            current_site = get_current_site(request)
            email_subject = f'[LaRegina] - Réinitialiser votre mot de passe'

            message = render_to_string(
                'account/email/password_reset_key_message.txt',
                {
                    'domain': current_site,
                    'scheme': request.scheme,
                    'uidb64': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': PasswordResetTokenGenerator().make_token(user)
                }
            )

            email_message = EmailMessage(
                email_subject, message,
                settings.EMAIL_HOST_USER,
                [email]
            )

            EmailThread(email_message).start()

        messages.success(
            request, f"""Nous vous avons envoyé un courriel à
            <strong>{email.lower()}</strong> contenant les
            instructions sur la façon de réinitialiser votre mot de passe.
            Consultez votre boîte de réception et cliquez sur le lien fourni.
            """
        )

        ctx = {'page_title': "Réinitialisation du mot de passe"}

        return render(request, self.template_name, ctx)


account_request_password_reset_view = AccountRequestPasswordResetView.as_view()


class AccountSetNewPasswordView(generic.View):

    template_name = "account/password_reset_email.html"

    def get(self, request, uidb64, token):

        context = {
            'uidb64': uidb64,
            'token': token,
            'page_title': "Aide avec le mot de passe",
        }

        try:
            user_id = force_str(urlsafe_base64_decode(uidb64))
            user = get_user_model().objects.get(pk=user_id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                messages.info(
                    request,
                    """Le lien de réinitialisation du mot de passe
                    n'est pas valide, veuillez en demander un nouveau."""
                )
                return render(request, self.template_name)

        except DjangoUnicodeDecodeError as identifier:
            messages.success(
                request, 'Lien invalide !')
            return render(request, self.template_name)

        return render(request, 'account/set_new_password.html', context)

    def post(self, request, uidb64, token):
        context = {
            'uidb64': uidb64,
            'token': token,
            'has_error': False
        }

        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        if len(password) < 6:
            messages.add_message(
                request, messages.ERROR,
                'les mots de passe doivent comporter au moins 6 caractères.'
            )
            context['has_error'] = True
        if password != password2:
            messages.add_message(
                request, messages.ERROR,
                'les mots de passe ne correspondent pas.'
            )
            context['has_error'] = True

        if context['has_error'] == True:
            return render(
                request, 'account/set_new_password.html',
                context
            )

        try:
            user_id = force_str(urlsafe_base64_decode(uidb64))

            user = get_user_model().objects.get(pk=user_id)
            user.set_password(password)
            user.save()

            messages.success(
                request,
                """
                    Réinitialisation du mot de passe réussie,
                    vous pouvez vous connecter avec un nouveau mot de passe.
                """
            )

            return redirect(reverse(settings.LOGIN_URL))

        except DjangoUnicodeDecodeError as identifier:
            messages.error(request, 'Lien invalide.')
            return render(
                request,
                'account/set_new_password.html',
                context
            )

        return render(request, 'account/set_new_password.html', context)


account_set_new_password_view = AccountSetNewPasswordView.as_view()


def logout_view(request):
    logout(request)
    messages.add_message(request, messages.SUCCESS, 'Vous vous êtes déconnecté.')
    return redirect(reverse(settings.LOGIN_URL))


logout_view = logout_view
