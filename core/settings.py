# core/settings.py

import os
from pathlib import Path
from decouple import config
from django.contrib.messages import constants as messages


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = TEMPLATE_DEBUG = config('DEBUG', default=True, cast=bool)
DEFAULT_CHARSET = 'UTF-8'
SITE_DESCRIPTION = ""
INDEX_DESCRIPTION = "Vendez sur LaRegina"
META_KEYWORDS = 'créer boutique vente ligne, vente, achat, laregina, deals, acheter, vendre, boutique, ouvrir un magasin en ligne'
SITE_NAME = 'LaRegina Deals'
APPEND_SLASH = True

# Custom Django auth settings
AUTH_USER_MODEL = 'accounts.User'

# site ID for allauth
SITE_ID = 1

# DJANGO-ADMIN CONFIGURATION
# Location of root django.contrib.admin URL
ADMIN_URL = 'lrg-admin/'

# See: https://docs.djangoproject.com/en/1.11/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []


# See: https://docs.djangoproject.com/en/1.11/ref/settings/#installed-apps
INSTALLED_APPS = [

    'django.contrib.auth',
    'django.contrib.sites',

    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django.contrib.humanize',
    'django.contrib.admin',

    'django.contrib.sitemaps',
]

OTHERS_APPS = [

    'crispy_forms',

    'allauth',
    'allauth.account',

    'django_countries',
    'phonenumber_field',
    'phonenumbers',
    'mptt',
]

LOCAL_APPS = [
    'search.apps.SearchConfig',
    'accounts.apps.AccountsConfig',
    'category.apps.CategoryConfig',
    'catalogue.apps.CatalogueConfig',
    'reviews.apps.ReviewsConfig',
    'cart.apps.CartConfig',
    'checkout.apps.CheckoutConfig',
    'analytics.apps.AnalyticsConfig',
    'pages.apps.PagesConfig',
    'caching',
]

INSTALLED_APPS += OTHERS_APPS + LOCAL_APPS

# AUTHENTICATION CONFIGURATION
AUTHENTICATION_BACKENDS = [
    # 'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

# Les utilisateurs connectés sont redirigés ici s'ils
# consultent les pages de connexion/inscription
LOGOUT_URL = 'home'
LOGIN_URL = 'account_login'
LOGIN_REDIRECT_URL = 'seller:profile'
SIGNUP_CUSTOMER_URL = 'customer_signup'

# Configuration django-allauth
# https://django-allauth.readthedocs.io/en/latest/configuration.html

ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_LOGOUT_ON_GET = True
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_MIN_LENGTH = 4
ACCOUNT_SESSION_REMEMBER = False
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_USER_MODEL_EMAIL_FIELD = 'email'
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_LOGOUT_REDIRECT_URL = LOGOUT_URL
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 7
ACCOUNT_AUTHENTICATED_LOGIN_REDIRECTS = True
# ACCOUNT_DEFAULT_HTTP_PROTOCOL = ''
ACCOUNT_EMAIL_CONFIRMATION_ANONYMOUS_REDIRECT_URL = LOGIN_URL
ACCOUNT_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL = LOGIN_REDIRECT_URL
ACCOUNT_EMAIL_SUBJECT_PREFIX = "LaRegina Deals <no-reply@laregina.deals>"

ACCOUNT_FORMS = {
    'login': 'accounts.forms.MarketLoginForm',
    'signup': 'accounts.forms.MarketSignupForm',
}

# La valeur d'affichage de l'utilisateur est le nom du profil associé
ACCOUNT_USER_DISPLAY = lambda user: user.shipping_first_name

EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp-relay.sendinblue.com'
EMAIL_HOST_USER = 'flavienhgs@gmail.com'
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
SENDGRID_API_KEY = config('SENDGRID_API_KEY', default='')
DEFAULT_FROM_EMAIL = SERVER_EMAIL = 'hello@laregina.com'

# Pour le développement, envoyer tous les courriers électroniques
# à la console au lieu de les envoyer
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# https://docs.djangoproject.com/fr/3.0/ref/settings/
# Let's Encrypt ssl/tls https

CACHE_TTL = 60 * 15
CACHE_TIMEOUT = 60 * 60

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',

    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.http.ConditionalGetMiddleware',
    'django.middleware.common.CommonMiddleware',
]

ROOT_URLCONF = 'core.urls'

# See: https://docs.djangoproject.com/en/1.11/ref/settings/#templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.csrf',
                'django.contrib.messages.context_processors.messages',

                # Custom context processors
                'core.context.context',
                'core.context.category',
                'core.context.cart_items',
                'accounts.context.profile',
            ],

            'debug': DEBUG,
        },
    },
]

# Configuration django-jet
# https://jet.readthedocs.io/en/latest/config_file.html

# See: http://django-crispy-forms.readthedocs.io/en/latest/install.html#template-packs
CRISPY_TEMPLATE_PACK = 'bootstrap4'

# See: https://docs.djangoproject.com/en/1.11/ref/settings/#wsgi-application
WSGI_APPLICATION = 'core.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': config('DATABASE_NAME'),
        'USER': config('DATABASE_USER'),
        'PASSWORD': config('DATABASE_PASSWORD'),
        'HOST': config('DATABASE_HOST', cast=str),
        'PORT': config('DATABASE_PORT', cast=int),
        'OPTIONS': {
            "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",
        }
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
        'OPTIONS': {'max_similarity': 0.9,}
    },
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {'min_length': 9,}
    },
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]

# password hashers
# https://docs.djangoproject.com/fr/3.1/topics/auth/passwords/

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
]

# Hashage des donnees
# https://docs.djangoproject.com/fr/3.1/ref/settings/
DEFAULT_HASHING_ALGORITHM = 'sha1'


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'UTC'
USE_I18N = USE_L10N = USE_TZ = True
DATE_INPUT_FORMATS = ('%d/%m/%Y', '%Y-%m-%d')

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/
# See: https://docs.djangoproject.com/en/1.11/ref/settings/#static-root

MEDIA_URL = '/media/'
STATIC_URL = '/static/'
MEDIA_ROOT = BASE_DIR / 'media'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

# staticfiles finders
# See: https://docs.djangoproject.com/en/1.11/ref/contrib/staticfiles/#staticfiles-finders

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

# Activez le backend de stockage WhiteNoise qui se charge de compresser
# les fichiers statiques et de créer des noms uniques pour chaque version
# afin qu'ils puissent être mis en cache à jamais en toute sécurité.
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Messages built-in framework

MESSAGE_TAGS = {
    messages.DEBUG: 'alert-secondary',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
}

MPTT_ADMIN_LEVEL_INDENT = 20

# https://django-redis-cache.readthedocs.io/en/latest/intro_quick_start.html
# https://pypi.org/project/django-redis/


# phonenumber config
PHONENUMBER_DEFAULT_REGION = "CI"
PHONENUMBER_DB_FORMAT = "NATIONAL"

# CINETPAY API KEY
CINETPAY_API_KEY = config('CINETPAY_API_KEY')
CINETPAY_SITE_ID = config('CINETPAY_SITE_ID')
CINETPAY_TRANS_ID = config('CINETPAY_TRANS_ID')

# Mailchimp Configuration
MAILCHIMP_API_KEY = config('MAILCHIMP_API_KEY')
MAILCHIMP_SUBSCRIBE_LIST_ID = config('MAILCHIMP_SUBSCRIBE_LIST_ID')

# Django est passé à la sérialisation JSON pour des raisons de sécurité, mais il ne
# sérialise pas les modèles. Nous devrions résoudre ce problème en étendant la
# django/core/serializers/json.Serializer pour avoir la fonction de `dumps`.
# dans tests/config.py
SESSION_SERIALIZER = 'django.contrib.sessions.serializers.JSONSerializer'
