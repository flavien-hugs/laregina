import os

from .base import *  # noqa


abspath = os.path.abspath(__file__)
dirname = os.path.dirname(os.path.dirname(abspath))
BASE_DIR = os.path.dirname(dirname)


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "dev.sqlite3"),
        "CONN_MAX_AGE": 500,
    }
}

ADMIN_URL = "admin/"
