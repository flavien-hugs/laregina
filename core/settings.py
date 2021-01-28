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
SECRET_KEY = config('SECRET_KEY', default='_q@t!jz_mb@j_l64kk%_7!(+d3o4fa)qpc!fmgzem3z)4)l-&w')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = TEMPLATE_DEBUG = config('DEBUG', default=True, cast=bool)
DEFAULT_CHARSET = 'UTF-8'
SITE_DESCRIPTION = ""
INDEX_DESCRIPTION = "Vender sur LaRegina"
META_KEYWORDS = ''
SITE_NAME = 'LaRegina Deals'
USE_THOUSAND_SEPARATOR = True
THOUSAND_SEPARATOR = ' '
APPEND_SLASH = True

ADMINS = (
    #(, )
)

MANAGERS = ADMINS

# DJANGO-ADMIN CONFIGURATION
# Location of root django.contrib.admin URL
ADMIN_URL = 'admin/'

# See: https://docs.djangoproject.com/en/1.11/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []


# See: https://docs.djangoproject.com/en/1.11/ref/settings/#installed-apps
INSTALLED_APPS = [
    # for authorization and registration
    
    'django.contrib.auth',
    'django.contrib.sites',

    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django.contrib.humanize',
    'django.contrib.admin',

    'django.contrib.sitemaps',
    'django.contrib.redirects',    
]

OTHERS_APPS = [
    'crispy_forms',

    'allauth',
    'allauth.account',

    'django_filters',
    'django_countries',
    'phonenumber_field',
    'phonenumbers',
    'tagulous',
    'mptt',
]

LOCAL_APPS = [
    'accounts.apps.AccountsConfig',
    'category.apps.CategoryConfig',
    'catalogue.apps.CatalogueConfig',
    'reviews.apps.ReviewsConfig',
    'cart.apps.CartConfig',
    'order.apps.OrderConfig',
    'search.apps.SearchConfig',
    'analytics.apps.AnalyticsConfig',
    'pages.apps.PagesConfig',
    'caching',
]

INSTALLED_APPS += OTHERS_APPS + LOCAL_APPS

# Custom Django auth settings
AUTH_USER_MODEL = 'accounts.User'

# Site ID for allauth
SITE_ID = 1
# SITE_ID = config('SITE_ID', cast=int)

# AUTHENTICATION CONFIGURATION
AUTHENTICATION_BACKENDS = [
    # 'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

# Les utilisateurs connectés sont redirigés ici s'ils consultent les pages de connexion/inscription
LOGIN_URL = 'account_login'
LOGIN_REDIRECT_URL = 'seller:profile'
    

# Ne pas afficher la confirmation de déconnexion
ACCOUNT_LOGOUT_ON_GET = True

# Configuration django-allauth
# https://django-allauth.readthedocs.io/en/latest/configuration.html

ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_SESSION_REMEMBER = 'yes'
ACCOUNT_USERNAME_MIN_LENGTH = 4
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_USER_MODEL_EMAIL_FIELD = 'email'
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 7
ACCOUNT_USER_MODEL_USERNAME_FIELD = 'username'
ACCOUNT_EMAIL_CONFIRMATION_ANONYMOUS_REDIRECT_URL = 'account_login'
ACCOUNT_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL = 'account_login'
ACCOUNT_EMAIL_SUBJECT_PREFIX = "LaRegina Deals <infos@laregina-ci.com>"

ACCOUNT_FORMS = {
    'login': 'accounts.forms.LoginForm',
    'signup': 'accounts.forms.MarketSignupForm',
}

# La valeur d'affichage de l'utilisateur est le nom du profil associé
ACCOUNT_USER_DISPLAY = lambda user: user.name

EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp-relay.sendinblue.com'
EMAIL_HOST_USER = 'flavienhgs@gmail.com'
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
SENDGRID_API_KEY = config('SENDGRID_API_KEY', default='')

# Pour le développement, envoyer tous les courriers électroniques
# à la console au lieu de les envoyer
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# https://docs.djangoproject.com/fr/3.0/ref/settings/
# Let's Encrypt ssl/tls https
SECURE_FRAME_DENY = True
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_NAME = 'cookies'
SESSION_COOKIE_DAYS = 90
SESSION_COOKIE_AGE = 60 * 60 * 24 * SESSION_COOKIE_DAYS 
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_COOKIE_SECURE = True
CACHE_MIDDLEWARE_ALIAS = 'default'
CACHE_MIDDLEWARE_SECONDS = 600
CACHE_MIDDLEWARE_KEY_PREFIX = ''
CACHE_TIMEOUT = 60 * 60

# Upon deployment, change to True
ENABLE_SSL = False

MIDDLEWARE = [
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'core.SSLMiddleware.SSLRedirect',
    'django.contrib.redirects.middleware.RedirectFallbackMiddleware',

    # Custom middleware
    # 'accounts.middleware.UserProfileMiddleware',
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
                'accounts.context.customization',
            ],

            'debug': DEBUG,
        },
    },
]
# See: http://django-crispy-forms.readthedocs.io/en/latest/install.html#template-packs
CRISPY_TEMPLATE_PACK = 'bootstrap4'

# See: https://docs.djangoproject.com/en/1.11/ref/settings/#wsgi-application
WSGI_APPLICATION = 'core.wsgi.application'

ANALYTICS_TRACKING_ID = ''
PRODUCT_PER_PAGE = 1
PRODUCT_PER_ROW = 4

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
        'ATOMIC_REQUESTS': True
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

import lzma

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            'PICKLE_VERSION': -1,
            'PASSWORD': config('REDIS_PASSWORD'),
            "COMPRESSOR": "django_redis.compressors.lzma.LzmaCompressor",
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            'COMPRESSOR_CLASS_KWARGS': {'level': 5,},
            "SOCKET_CONNECT_TIMEOUT" : 5 ,
            "SOCKET_TIMEOUT" : 5 ,
        },

        "KEY_PREFIX": "caching"
    }
}

# Cache time to live is 15 minutes.
CACHE_TTL = 60 * 15
DJANGO_REDIS_IGNORE_EXCEPTIONS = True

# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     "handlers": {
#         "file": {
#             "level": "INFO",
#             "class": "logging.handlers.TimedRotatingFileHandler",
#             "filename": BASE_DIR / "logs/debug.log",
#             "when": "D",
#             "interval": 1,
#             "backupCount": 100,
#         }
#     },

#     'loggers': {
#         "django": {
#             "handlers": ["file"],
#             "level": "INFO",
#             "propagate": True
#         },

#         "project": {
#             "handlers": ["file"],
#             "level": "INFO",
#             "propagate": True
#         },

#         "": {
#             "handlers": ["file"],
#             "level": "INFO",
#             "propagate": True
#         },
#     },
# }

# phonenumber config
PHONENUMBER_DEFAULT_REGION = "CI"
PHONENUMBER_DB_FORMAT = "NATIONAL"

# à utiliser avec l'URL Canonicalization Middleware:
# c'est le nom d'hôte canonique à utiliser par l'application (obligatoire)
CANON_URL_HOST = 'www.your-domain.com'

# voici les noms d'hôtes qui seront redirigés vers le CANON_URL_HOSTNAME 
# (facultatif; s'il n'est pas fourni, tout ce qui ne correspond pas sera redirigé)
CANON_URLS_TO_REWRITE = ['your-domain.com', 'other-domain.com']

# Google Checkout API credentials
GOO_URL = config('GOO_URL')
GOOGLE_CHECKOUT_MERCHANT_ID = config('GOOGLE_CHECKOUT_MERCHANT_ID')
GOOGLE_CHECKOUT_MERCHANT_KEY = config('GOOGLE_CHECKOUT_MERCHANT_KEY')
GOOGLE_CHECKOUT_URL = GOO_URL + GOOGLE_CHECKOUT_MERCHANT_ID

# Authorize.Net API Credentials
AUTHNET_POST_URL = 'test.authorize.net'
AUTHNET_POST_PATH = '/gateway/transact.dll'
AUTHNET_LOGIN = ''
AUTHNET_KEY = ''

# Mailchimp Configuration
MAILCHIMP_API_KEY = config('MAILCHIMP_API_KEY')
MAILCHIMP_SUBSCRIBE_LIST_ID = config('MAILCHIMP_SUBSCRIBE_LIST_ID')

# Django est passé à la sérialisation JSON pour des raisons de sécurité, mais il ne
# sérialise pas les modèles. Nous devrions résoudre ce problème en étendant la
# django/core/serializers/json.Serializer pour avoir la fonction de `dumps`.
# dans tests/config.py
SESSION_SERIALIZER = 'django.contrib.sessions.serializers.JSONSerializer'
