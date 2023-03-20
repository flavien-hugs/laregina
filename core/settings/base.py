import re
import os
from pathlib import Path
from django.contrib.messages import constants as messages

import pyzstd
from dotenv import dotenv_values

env = dotenv_values(".env")

abspath = os.path.abspath(__file__)
dirname = os.path.dirname(os.path.dirname(abspath))
BASE_DIR = os.path.dirname(dirname)

PWA_SERVICE_WORKER_PATH = os.path.join(BASE_DIR, "static/js", "serviceworker.js")

DEBUG = env.get("DEBUG")
TEMPLATE_DEBUG = DEBUG

APPEND_SLASH = True
USE_THOUSAND_SEPARATOR = False
SECRET_KEY = env.get("SECRET_KEY")

SITE_DESCRIPTION = "Vente et achat en ligne Informatiques, Électromenager, Habillement et mode, Téléphones, TV, Jeux Vidéos"
INDEX_DESCRIPTION = "Vente et achat en ligne Informatiques, Électromenager, Habillement et mode, Téléphones, TV, Jeux Vidéos"
META_KEYWORDS = "créer boutique vente ligne, vente, achat, laregina, deals, acheter, vendre, boutique en ligne, laregina deals, ouvrir un magasin en ligne"

SITE_NAME = "LaRegina"
ADMIN_URL = "lrg-admin/"
AUTH_USER_MODEL = "accounts.User"

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
    "django.contrib.sitemaps",
    "django.contrib.sites",
]

OTHERS_APPS = [
    "jet",
    "django.contrib.admin",
    "crispy_forms",
    "phonenumber_field",
    "phonenumbers",
    "mptt",
    "django_summernote",
    "compressor",
    "dbbackup",
    "django_crontab",
    "pwa",
]

LOCAL_APPS = [
    "accounts.apps.AccountsConfig",
    "search.apps.SearchConfig",
    "category.apps.CategoryConfig",
    "catalogue.apps.CatalogueConfig",
    "reviews.apps.ReviewsConfig",
    "cart.apps.CartConfig",
    "checkout.apps.CheckoutConfig",
    "voucher.apps.VoucherConfig",
    "analytics.apps.AnalyticsConfig",
    "pages.apps.PagesConfig",
    "caching",
]

INSTALLED_APPS += LOCAL_APPS + OTHERS_APPS

SITE_ID = 1

LOGOUT_URL = "/"
LOGOUT_REDIRECT_URL = "/"

LOGIN_URL = "auth_views:account_login"
SIGNUP_URL = "auth_views:account_signup"
LOGIN_REDIRECT_URL = "dashboard_seller:profile"

EMAIL_HOST = env.get("EMAIL_HOST")
EMAIL_PORT = env.get("EMAIL_PORT")
EMAIL_USE_TLS = env.get("EMAIL_USE_TLS")
EMAIL_HOST_USER = env.get("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = env.get("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = SERVER_EMAIL = "LaRegina <no-reply@laregina.deals>"

MIDDLEWARE = [
    # "django.middleware.cache.UpdateCacheMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.common.BrokenLinkEmailsMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.gzip.GZipMiddleware",
    "django.middleware.http.ConditionalGetMiddleware",
    # "django.middleware.cache.FetchFromCacheMiddleware",
]

ROOT_URLCONF = "core.urls"

TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [TEMPLATES_DIR],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.csrf",
                "django.contrib.messages.context_processors.messages",
                "helpers.context.context",
                "helpers.context.category",
                "helpers.context.cart_items",
                "accounts.context.profile",
            ]
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"

CSRF_COOKIE_HTTPONLY = True
SESSION_COOKIE_HTTPONLY = True
X_FRAME_OPTIONS = "SAMEORIGIN"

CRISPY_TEMPLATE_PACK = "bootstrap4"

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
        "OPTIONS": {
            "max_similarity": 0.9,
        },
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {
            "min_length": 9,
        },
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
]

DEFAULT_HASHING_ALGORITHM = "sha1"

USE_TZ = False
TIME_ZONE = "UTC"
LANGUAGE_CODE = "fr-fr"
USE_I18N = USE_L10N = True
DATE_INPUT_FORMATS = ("%d/%m/%Y", "%Y-%m-%d")

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]

STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "compressor.finders.CompressorFinder",
]

WHITENOISE_KEEP_ONLY_HASHED_FILES = True
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MESSAGE_TAGS = {
    messages.DEBUG: "alert-secondary",
    messages.INFO: "alert-info",
    messages.SUCCESS: "alert-success",
    messages.WARNING: "alert-warning",
    messages.ERROR: "alert-danger",
}

MPTT_ADMIN_LEVEL_INDENT = 20

PHONENUMBER_DEFAULT_REGION = "CI"
PHONENUMBER_DB_FORMAT = "INTERNATIONAL"
PHONENUMBER_DEFAULT_FORMAT = "INTERNATIONAL"

CINETPAY_API_KEY = env.get("CINETPAY_API_KEY")
CINETPAY_SITE_ID = env.get("CINETPAY_SITE_ID")
CINETPAY_TRANS_ID = env.get("CINETPAY_TRANS_ID")

SESSION_SERIALIZER = "django.contrib.sessions.serializers.JSONSerializer"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

IGNORABLE_404_URLS = [
    re.compile(r"^/apple-touch-icon.*\.png$"),
    re.compile(r"^/favicon\.ico$"),
    re.compile(r"^/robots\.txt$"),
]

JET_THEMES = [{"theme": "light-gray", "color": "#222", "title": "Light Gray"}]

JET_SIDE_MENU_COMPACT = True
JET_CHANGE_FORM_SIBLING_LINKS = True

SUMMERNOTE_THEME = "bs4"

SUMMERNOTE_CONFIG = {
    "iframe": True,
    "summernote": {
        "airMode": False,
        "width": "100%",
        "height": "300",
        "toolbar": [
            ["font", ["bold", "italic", "underline", "clear"]],
            ["fontname", ["fontname"]],
            ["color", ["color"]],
            ["para", ["ul", "ol", "paragraph"]],
            ["height", ["height"]],
            ["table", ["table"]],
            ["insert", ["picture", "hr"]],
            ["view", ["fullscreen"]],
        ],
        "attachment_absolute_uri": True,
        "attachment_require_authentication": True,
        "attachment_storage_class": "core.utils.upload_image_path",
        "codemirror": {
            "mode": "htmlmixed",
            "lineNumbers": "true",
            "theme": "monokai",
        },
    },
}

CACHE_TTL = 60 * 15
CACHE_TIMEOUT = 60 * 60

REDIS_PORT = env.get("REDIS_PORT")
REDIS_HOST = env.get("REDIS_HOST")

SESSION_ENGINE = "django.contrib.sessions.backends.cache"

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"redis://{REDIS_HOST}:{REDIS_PORT}",
        "OPTIONS": {
            "db": "10",
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "parser_class": "redis.connection.PythonParser",
            "pool_class": "redis.BlockingConnectionPool",
        },
    }
}

CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60
BROKER_URL = env.get("CELERY_BROKER_REDIS_URL")

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

DBBACKUP_STORAGE = "django.core.files.storage.FileSystemStorage"
DBBACKUP_STORAGE_OPTIONS = {"location": os.path.join(BASE_DIR, "db_backup")}

CRONJOBS = [("0 24 * * *", "helpers.cron.create_backups_scheduled_job")]

SENDER_ID = env.get("SENDER_ID")
API_TOKEN = env.get("API_TOKEN")
SMS_API_KEY = env.get("SMS_API_KEY")

PWA_APP_NAME = SITE_NAME
PWA_APP_DESCRIPTION = SITE_DESCRIPTION
PWA_APP_THEME_COLOR = "#000000"
PWA_APP_BACKGROUND_COLOR = "#ffffff"
PWA_APP_DISPLAY = "standalone"
PWA_APP_SCOPE = "/"
PWA_APP_ORIENTATION = "any"
PWA_APP_START_URL = "/"
PWA_APP_STATUS_BAR_COLOR = "default"
PWA_APP_ICONS = [{"src": "static/img/logo_laregina.png", "sizes": "160x160"}]
PWA_APP_ICONS_APPLE = [{"src": "static/img/logo_laregina.png", "sizes": "160x160"}]
PWA_APP_SPLASH_SCREEN = [
    {
        "src": "static/img/logo_laregina.png",
        "media": "(device-width: 320px) and (device-height: 568px) and (-webkit-device-pixel-ratio: 2)",
    }
]
PWA_APP_DIR = "ltr"
PWA_APP_LANG = "fr-FR"
