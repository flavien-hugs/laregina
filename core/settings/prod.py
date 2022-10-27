from .base import *  # noqa


PREPEND_WWW = True
APPEND_SLASH = True

ALLOWED_HOSTS = [
    '*.laregina.deals',
    'laregina.deals',
    'www.laregina.deals'
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': env.get('DATABASE_NAME'),
        'USER': env.get('DATABASE_USER'),
        'PASSWORD': env.get('DATABASE_PASSWORD'),
        'HOST': env.get('DATABASE_HOST'),
        'PORT': env.get('DATABASE_PORT'),
    }
}

SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 86400
SECURE_HSTS_PRELOAD = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = False

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    "handlers": {
        "file": {
            "level": "INFO",
            "class": "logging.handlers.TimedRotatingFileHandler",
            "filename": os.path.join(BASE_DIR, 'logs/debug.log'),
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
