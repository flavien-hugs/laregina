from .base import *  # noqa


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "dev.sqlite3"),
        "CONN_MAX_AGE": 500,
    }
}

ADMIN_URL = "admin/"
