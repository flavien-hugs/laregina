# core/production.py

import dj_database_url
from core.settings import *

DEBUG = TEMPLATE_DEBUG = False
ALLOWED_HOSTS = [
    'laregina.deals',
    'www.laregina.deals'
]

# Parse database configuration from $DATABASE_URL
# Change 'default' database configuration with
# $DATABASE_URL. pwd=__unstainc@@ bdd=c1581337c_laregina_deals_db
# username=c1581337c_unsta_dev

DATABASES['default'].update(
    dj_database_url.config(
        conn_max_age=500, ssl_require=True)
    )

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': config('DATABASE_NAME'),
        'USER': config('DATABASE_USER'),
        'PASSWORD': config('DATABASE_PASSWORD'),
        'HOST': config('DATABASE_HOST', cast=str),
        'PORT': config('DATABASE_PORT', cast=int),
        'ATOMIC_REQUESTS': True,
        'OPTIONS': {
            "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",
        }
    }
}

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

USE_X_FORWARDED_HOST = True
CORS_REPLACE_HTTPS_REFERER = True

SECURE_SSL_HOST = BASE_URL
SECURE_FRAME_DENY = True
SECURE_SSL_REDIRECT = True
SECURE_HSTS_PRELOAD = True
SECURE_REDIRECT_EXEMPT = []
SECURE_HSTS_SECONDS = 15768000
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_REFERRER_POLICY = 'origin-when-cross-origin'
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# gestion interdomaine
CSRF_COOKIE_DOMAIN = 'https://www.laregina.deals'

# Simplified static file serving.
# https://warehouse.python.org/project/whitenoise/
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
