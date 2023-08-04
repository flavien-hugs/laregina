from django.urls import reverse
from django.conf import settings
from django.views import generic
from django.utils import timezone
from django.contrib import messages
from django.shortcuts import redirect, render
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import DjangoUnicodeDecodeError, force_str
from django.contrib.auth import authenticate, get_user_model, login, logout

from helpers.utils import SendEmail
from accounts.mixins import login_required_redirect
from accounts.forms import (
    AccountLoginForm,
    AccountRegisterForm,
    AccountRequestPasswordResetForm,
)


User = get_user_model()


class AccountSignupView(generic.View):
    form_class = AccountRegisterForm
    template_name = "account/signup.html"

    @login_required_redirect
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class()
        ctx = {"form": form, "page_title": "Créer votre compte"}
        return render(request, self.template_name, ctx)

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Compte créé avec succès. Veuillez vous connecter à votre tableau de bord !",
            )
            return redirect(reverse(settings.LOGIN_REDIRECT_URL))
        messages.error(request, "Veuillez vérifier les informations fournies !")

        ctx = {"form": form, "page_title": "Créer votre compte"}
        return render(request, self.template_name, ctx)


account_signup_view = AccountSignupView.as_view()


class AccountLoginView(generic.View):
    form_class = AccountLoginForm
    template_name = "account/login.html"

    @login_required_redirect
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class()
        ctx = {"form": form, "page_title": "Connexion"}
        return render(request, self.template_name, ctx)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]

            user = authenticate(email=email, password=password)

            if user is not None and user.is_active:
                user.last_login = timezone.now()
                user.save()
                login(request, user)
                messages.success(
                    request, f"Vous êtes connecté en tant que {user.email}!r"
                )
                return redirect(reverse(settings.LOGIN_REDIRECT_URL))
        messages.error(request, "Identifiants invalides ou compte désactivé !")

        page_title = "Connexion"
        context = {"form": form, "page_title": page_title}
        return render(request, self.template_name, context)


account_login_view = AccountLoginView.as_view()


class AccountRequestPasswordResetView(generic.View):
    form_class = AccountRequestPasswordResetForm
    template_name = "account/password_reset.html"

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        ctx = {"form": form, "page_title": "Réinitialisation du mot de passe"}
        return render(request, self.template_name, ctx)

    @login_required_redirect
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            email = form.cleaned_data.get("email")
            mail_to_lower = email.lower()
            user_data = User.filter_by_email(email=mail_to_lower)

            if user_data.exists():
                user = User.filter_by_email(email=mail_to_lower).get()

                SendEmail.send_confirmation_link(
                    request=request,
                    user=user,
                    template="account/email/password_reset_key_message.html",
                    subject="[LaRegina] - Réinitialiser votre mot de passe",
                )

                messages.success(
                    request,
                    f"Nous vous avons envoyé un courriel à \
                        {email.lower()} contenant les \
                        instructions sur la façon de réinitialiser votre mot de passe. \
                        Consultez votre boîte de réception et cliquez sur le lien fourni.",
                )
            else:
                messages.error(
                    request,
                    "L'utilisateur ayant cette adresse email \
                    n'existe pas.",
                )

        ctx = {"form": form, "page_title": "Réinitialisation du mot de passe"}
        return render(request, self.template_name, ctx)


account_request_password_reset_view = AccountRequestPasswordResetView.as_view()


class AccountSetNewPasswordView(generic.View):
    template_name = "account/password_reset.html"

    def get(self, request, uidb64, token):
        context = {
            "uidb64": uidb64,
            "token": token,
            "page_title": "Modifier votre mot de passe",
        }

        try:
            user_id = force_str(urlsafe_base64_decode(uidb64))
            user = User.filter_by_id(pk=user_id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                messages.info(
                    request,
                    """Le lien de réinitialisation du mot de passe n'est pas valide, veuillez demander un nouveau lien.""",
                )
                return render(request, self.template_name)
        except DjangoUnicodeDecodeError:
            messages.success(request, "Lien invalide !")
            return render(request, self.template_name)

        return render(request, "account/set_new_password.html", context)

    def post(self, request, uidb64, token):
        context = {"uidb64": uidb64, "token": token}

        password = request.POST.get("password")
        password2 = request.POST.get("password2")

        if len(password) < 6:
            messages.add_message(
                request,
                messages.ERROR,
                "les mots de passe doivent comporter au moins 6 caractères.",
            )

        if password != password2:
            messages.add_message(
                request, messages.ERROR, "les mots de passe ne correspondent pas."
            )

        template = "account/set_new_password.html"
        return render(request, template, context)

        try:
            user_id = force_str(urlsafe_base64_decode(uidb64))
            user = User.filter_by_id(pk=user_id)
            user.set_password(password)
            user.save()

            messages.success(
                request,
                """
                    Réinitialisation du mot de passe réussie,
                    vous pouvez vous connecter avec un nouveau mot de passe.
                """,
            )

            return redirect(reverse(settings.LOGIN_URL))

        except DjangoUnicodeDecodeError:
            messages.error(request, "Lien invalide.")
            return render(request, template, context)

        return render(request, template, context)


account_set_new_password_view = AccountSetNewPasswordView.as_view()


def logout_view(request):
    logout(request)
    messages.add_message(request, messages.SUCCESS, "Vous vous êtes déconnecté.")
    return redirect(reverse(settings.LOGIN_URL))


account_logout_view = logout_view
