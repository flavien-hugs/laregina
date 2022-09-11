# core/settings.py

import re
import os
from pathlib import Path
from django.contrib.messages import constants as messages

import pyzstd

from dotenv import dotenv_values

env = dotenv_values(".env")

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = env.get('SECRET_KEY')

DEBUG = True
TEMPLATE_DEBUG = DEBUG
DEFAULT_CHARSET = 'UTF-8'
SITE_DESCRIPTION = ""
INDEX_DESCRIPTION = "Vente et achat en ligne Informatiques, Électromenager, Habillement et mode, Téléphones, TV, Jeux Vidéos"
META_KEYWORDS = 'créer boutique vente ligne, vente, achat, laregina, deals, acheter, vendre, boutique en ligne, laregina deals, ouvrir un magasin en ligne'
SITE_NAME = 'LaRegina Deals'
APPEND_SLASH = True

AUTH_USER_MODEL = 'accounts.User'
ADMIN_URL = 'lrg-admin/'

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.auth',

    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django.contrib.humanize',
    'django.contrib.sitemaps',

    'django.contrib.sites',
]

OTHERS_APPS = [
    'jet',
    'django.contrib.admin',

    'crispy_forms',

    'allauth',
    'allauth.account',

    'django_countries',
    'phonenumber_field',
    'phonenumbers',
    'mptt',

    'django_summernote',
    'compressor',

    'dbbackup',
    'django_crontab',
]

LOCAL_APPS = [
    'accounts.apps.AccountsConfig',
    'search.apps.SearchConfig',
    'category.apps.CategoryConfig',
    'catalogue.apps.CatalogueConfig',
    'reviews.apps.ReviewsConfig',
    'cart.apps.CartConfig',
    'checkout.apps.CheckoutConfig',
    'voucher.apps.VoucherConfig',
    'analytics.apps.AnalyticsConfig',
    'pages.apps.PagesConfig',
    'caching',
]

INSTALLED_APPS += OTHERS_APPS + LOCAL_APPS

SITE_ID = 1

AUTHENTICATION_BACKENDS = [
    'allauth.account.auth_backends.AuthenticationBackend',
]

LOGOUT_URL = 'home'
LOGIN_URL = 'account_login'
LOGIN_REDIRECT_URL = 'seller:profile'
SIGNUP_CUSTOMER_URL = 'customer_signup'

# Configuration django-allauth
# https://django-allauth.readthedocs.io/en/latest/configuration.html

ACCOUNT_LOGOUT_ON_GET = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_MIN_LENGTH = 4
ACCOUNT_SESSION_REMEMBER = False
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_VERIFICATION = None
ACCOUNT_USER_MODEL_EMAIL_FIELD = 'email'
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_LOGOUT_REDIRECT_URL = LOGOUT_URL
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 7
ACCOUNT_AUTHENTICATED_LOGIN_REDIRECTS = True
ACCOUNT_EMAIL_CONFIRMATION_ANONYMOUS_REDIRECT_URL = LOGIN_URL
ACCOUNT_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL = LOGIN_REDIRECT_URL
ACCOUNT_EMAIL_SUBJECT_PREFIX = "LaRegina Deals <no-reply@laregina.deals>"

ACCOUNT_FORMS = {
    'login': 'accounts.forms.MarketLoginForm',
    'signup': 'accounts.forms.MarketSignupForm',
}

ACCOUNT_USER_DISPLAY = lambda user: user.shipping_first_name

EMAIL_HOST = env.get('EMAIL_HOST')
EMAIL_PORT = env.get('EMAIL_PORT')
EMAIL_USE_TLS = env.get('EMAIL_USE_TLS')
EMAIL_HOST_USER = env.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env.get('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = SERVER_EMAIL = 'no-reply@laregina.deals'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',

    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',

    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    "django.middleware.common.BrokenLinkEmailsMiddleware",
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'django.middleware.gzip.GZipMiddleware',
    'django.middleware.http.ConditionalGetMiddleware',
]

ROOT_URLCONF = 'core.urls'

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
                'helpers.context.context',
                'helpers.context.category',
                'helpers.context.cart_items',
                'accounts.context.profile',
            ],

            'debug': DEBUG,
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'

CSRF_COOKIE_HTTPONLY = True
SESSION_COOKIE_HTTPONLY = True
X_FRAME_OPTIONS = "SAMEORIGIN"

CRISPY_TEMPLATE_PACK = 'bootstrap4'

if DEBUG:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': str(BASE_DIR / 'db.sqlite3')
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': env.get('DATABASE_NAME'),
            'USER': env.get('DATABASE_USER'),
            'PASSWORD': env.get('DATABASE_PASSWORD'),
            'HOST': env.get('DATABASE_HOST'),
            'PORT': env.get('DATABASE_PORT'),
            'OPTIONS': {
                "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",
            }
        }
    }

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

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
]

DEFAULT_HASHING_ALGORITHM = 'sha1'

USE_TZ = False
TIME_ZONE = 'UTC'
LANGUAGE_CODE = 'fr-fr'
USE_I18N = USE_L10N = True
DATE_INPUT_FORMATS = ('%d/%m/%Y', '%Y-%m-%d')

MEDIA_URL = '/media/'
STATIC_URL = '/static/'
MEDIA_ROOT = BASE_DIR / 'media'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',

    'compressor.finders.CompressorFinder',
]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MESSAGE_TAGS = {
    messages.DEBUG: 'alert-secondary',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
}

MPTT_ADMIN_LEVEL_INDENT = 20

PHONENUMBER_DEFAULT_REGION = "CI"
PHONENUMBER_DB_FORMAT = "NATIONAL"
PHONENUMBER_DEFAULT_FORMAT = "NATIONAL"

CINETPAY_API_KEY = env.get('CINETPAY_API_KEY')
CINETPAY_SITE_ID = env.get('CINETPAY_SITE_ID')
CINETPAY_TRANS_ID = env.get('CINETPAY_TRANS_ID')

MAILCHIMP_API_KEY = env.get('MAILCHIMP_API_KEY')
MAILCHIMP_SUBSCRIBE_LIST_ID = env.get('MAILCHIMP_SUBSCRIBE_LIST_ID')

SESSION_SERIALIZER = 'django.contrib.sessions.serializers.JSONSerializer'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

IGNORABLE_404_URLS = [
    re.compile(r'^/apple-touch-icon.*\.png$'),
    re.compile(r'^/favicon\.ico$'),
    re.compile(r'^/robots\.txt$'),
]

JET_THEMES = [
    {
        'theme': 'light-gray',
        'color': '#222',
        'title': 'Light Gray'
    }
]

JET_SIDE_MENU_COMPACT = True
JET_CHANGE_FORM_SIBLING_LINKS = True

SUMMERNOTE_THEME = 'bs4'

SUMMERNOTE_CONFIG = {
    'iframe': True,

    'summernote': {
        'airMode': False,
        'width': '100%',
        'height': '300',
        'toolbar': [
            ['font', ['bold', 'italic', 'underline', 'clear']],
            ['fontname', ['fontname']],
            ['color', ['color']],
            ['para', ['ul', 'ol', 'paragraph']],
            ['height', ['height']],
            ['table', ['table']],
            ['insert', ['picture', 'hr']],
            ['view', ['fullscreen']],
        ],
        'attachment_absolute_uri': True,
        'attachment_require_authentication': True,
        'attachment_storage_class': 'core.utils.upload_image_path',

        'codemirror': {
            'mode': 'htmlmixed',
            'lineNumbers': 'true',
            'theme': 'monokai',
        },
    },
}

CACHE_TTL = 60 * 15
CACHE_TIMEOUT = 60 * 60

DJANGO_REDIS_IGNORE_EXCEPTIONS = True
DJANGO_REDIS_LOG_IGNORED_EXCEPTIONS = True

COMPRESS_ENABLED = True
COMPRESS_URL = STATIC_URL
COMPRESS_OUTPUT_DIR = "cache"
COMPRESS_STORAGE = "compressor.storage.GzipCompressorFileStorage"
COMPRESS_CSS_FILTERS = [
    "compressor.filters.css_default.CssAbsoluteFilter",
    "compressor.filters.cssmin.CSSMinFilter",
]
COMPRESS_JS_FILTERS = ["compressor.filters.jsmin.JSMinFilter"]
COMPRESS_REBUILD_TIMEOUT = 5400
COMPRESS_PRECOMPILERS = (
    ("text/less", "/usr/local/bin/lessc {infile} {outfile}"),
    ("text/x-sass", "/usr/local/bin/sass {infile} {outfile}"),
    ("text/x-scss", "/usr/local/bin/sass {infile} {outfile}"),
)
COMPRESS_OFFLINE_CONTEXT = {
    "STATIC_URL": "STATIC_URL",
}

DBBACKUP_STORAGE = 'django.core.files.storage.FileSystemStorage'
DBBACKUP_STORAGE_OPTIONS = {'location': BASE_DIR / 'db_backup'}

CRONJOBS = [
    ('0 24 * * *', 'helpers.cron.create_backups_scheduled_job')
]

SENDER_ID = env.get('SENDER_ID')
SMS_API_KEY = env.get('SMS_API_KEY')
