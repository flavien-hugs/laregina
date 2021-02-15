# core/production.py

import dj_database_url
from core.settings import *

DEBUG = TEMPLATE_DEBUG = False
BASE_URL = ''
ALLOWED_HOSTS = ['*.onrender.com']

# Parse database configuration from $DATABASE_URL
# Change 'default' database configuration with
# $DATABASE_URL.

DATABASES['default'].update(
    dj_database_url.config(
        conn_max_age=500, ssl_require=True)
    )

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

ENABLE_SSL = True
HOST_SCHEME = "https://"
X_FRAME_OPTIONS = 'DENY'
CSRF_USE_SESSIONS = True
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTONLY = True
# CSRF_FAILURE_VIEW = ''
SECURE_SSL_REDIRECT = True
SECURE_HSTS_PRELOAD = True
USE_X_FORWARDED_HOST = True
SECURE_HSTS_SECONDS = 15768000
SECURE_BROWSER_XSS_FILTER = True
CORS_REPLACE_HTTPS_REFERER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_REFERRER_POLICY = 'origin-when-cross-origin'
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# gestion interdomaine
CSRF_COOKIE_DOMAIN = ""

# Simplified static file serving.
# https://warehouse.python.org/project/whitenoise/
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
