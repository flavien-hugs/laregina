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

# 'django.middleware.security.SecurityMiddleware',
MIDDLEWARE += [
    'django.middleware.cache.UpdateCacheMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
]

# https://docs.djangoproject.com/fr/3.0/ref/settings/
# Let's Encrypt ssl/tls https

# https://docs.djangoproject.com/fr/3.0/ref/settings/
# Let's Encrypt ssl/tls https
SECURE_FRAME_DENY = True
SESSION_COOKIE_DAYS = 90
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_NAME = '__session__'
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_COOKIE_SAMESITE = 'Strict'
# SESSION_COOKIE_DOMAIN = 'test.laregina.deals'
SESSION_COOKIE_AGE = 60 * 60 * 24 * SESSION_COOKIE_DAYS
# SESSION_ENGINE = "django.contrib.sessions.backends.cache"

CACHE_MIDDLEWARE_SECONDS = 600
CACHE_MIDDLEWARE_KEY_PREFIX = ''
CACHE_MIDDLEWARE_ALIAS = 'default'

CSRF_USE_SESSIONS = True
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_NAME = '__lrg__'
# CSRF_COOKIE_DOMAIN = 'test.laregina.deals'

SECURE_SSL_REDIRECT = True
SECURE_HSTS_PRELOAD = True
SECURE_HSTS_SECONDS = 15768000
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_REFERRER_POLICY = 'origin-when-cross-origin'
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

ENABLE_SSL = True
HOST_SCHEME = "https://"
X_FRAME_OPTIONS = 'DENY'
# CSRF_FAILURE_VIEW = ''
USE_X_FORWARDED_HOST = True
CORS_REPLACE_HTTPS_REFERER = True

# Simplified static file serving.
# https://warehouse.python.org/project/whitenoise/
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
}

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