# core/production.py

from core.settings import *

PREPEND_WWW = True
DEBUG = TEMPLATE_DEBUG = False

ALLOWED_HOSTS = [
    '*.laregina.deals',
    'laregina.deals',
    'www.laregina.deals'
]

MEDIA_URL = '/media/'
STATIC_URL = '/static/'
MEDIA_ROOT = '/home/c1581337c/public_html/media'
STATIC_ROOT = '/home/c1581337c/public_html/static'
STATICFILES_DIRS = [BASE_DIR / 'assets']

# Parse database configuration from $DATABASE_URL
# Change 'default' database configuration with
# $DATABASE_URL. pwd=__unstainc@@ bdd=c1581337c_laregina_deals_db
# username=c1581337c_unsta_dev

# APPLICATION DEFINITION
INSTALLED_APPS += ['whitenoise.runserver_nostatic']

# https://docs.djangoproject.com/fr/3.0/ref/settings/
# Let's Encrypt ssl/tls https

SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 86400
SECURE_HSTS_PRELOAD = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

SESSION_COOKIE_SECURE = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = False

CSRF_USE_SESSIONS = True
CSRF_COOKIE_SECURE = True

# https://warehouse.python.org/project/whitenoise/
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    "handlers": {
        "file": {
            "level": "INFO",
            "class": "logging.handlers.TimedRotatingFileHandler",
            "filename": BASE_DIR / "logs/debug.log",
            "when": "D",
            "interval": 1,
            "backupCount": 100,
        }
    },

    'loggers': {
        "django": {
            "handlers": ["file"],
            "level": "INFO",
            "propagate": True
        },

        "project": {
            "handlers": ["file"],
            "level": "INFO",
            "propagate": True
        },

        "": {
            "handlers": ["file"],
            "level": "INFO",
            "propagate": True
        },
    },
}
