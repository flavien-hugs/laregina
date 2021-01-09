# core.utils.py

import os
import random
import string
import threading
from django.conf import settings
from django.utils.text import slugify
from django.core.validators import EmailValidator


def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def upload_image_path(instance, filename):
    new_filename = random.randint(1, 9347326742427)
    name, ext = get_filename_ext(filename)
    final_filename = "{new_filename}{ext}".format(new_filename=new_filename, ext=ext)
    return "{new_filename}/{final_filename}".format(
        new_filename=new_filename, final_filename=final_filename
    )


def email_validation_function(value):
    validator = EmailValidator()
    validator(value)
    return value


def generate_key():
    key = "".join(random.choices(string.digits, k=4))
    return key
