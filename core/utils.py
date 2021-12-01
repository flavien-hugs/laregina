# core.utils.py

import os
import string
import random
from django.utils.text import slugify
from django.core.validators import EmailValidator


def random_string_generator(size=8, carac=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(carac) for _ in range(size))

def unique_key_generator(instance):
    size = random.randint(20, 45)
    key = random_string_generator(size=size)
    Klass = instance.__class__
    qsx = Klass.objects.filter(key=key).exists()
    if qsx:
        return unique_slug_generator(instance)
    return key

def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext

def upload_image_logo_path(instance, filename):
    new_filename = slugify(instance.user.store)
    name, ext = get_filename_ext(filename)
    final_filename = f"{new_filename}-{instance.id}{ext}"
    return f"images/logo/{final_filename}"

def upload_image_path(instance, filename):
    new_filename = slugify(instance.product.name)
    name, ext = get_filename_ext(filename)
    final_filename = f"{new_filename}-{instance.id}{ext}"
    return f"images/produit/{final_filename}"

def upload_promotion_image_path(instance, filename):
    new_filename = slugify(instance.name)
    name, ext = get_filename_ext(filename)
    final_filename = f"{new_filename}-{instance.id}{ext}"
    return f"images/promotion/{final_filename}"

def email_validation_function(value):
    validator = EmailValidator()
    validator(value)
    return value

def generate_key():
    key = "".join(random.choices(string.digits, k=50))
    return key

def unique_slug_generator(instance, new_slug=None):
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.name) or slugify(instance.store)

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=slug).exists()
    
    if qs_exists:
        new_slug = "{slug}-{randstr}".format(slug=slug, randstr=random_string_generator(size=8))
        return unique_slug_generator(instance, new_slug=new_slug)
    return slug


def vendor_unique_slug_generator(instance, new_slug=None):
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.store)

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=slug).exists()
    
    if qs_exists:
        new_slug = "{slug}-{randstr}".format(slug=slug, randstr=random_string_generator(size=8))
        return unique_slug_generator(instance, new_slug=new_slug)
    return slug
