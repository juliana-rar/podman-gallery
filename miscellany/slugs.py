# -*- coding: utf-8 -*-

from django.utils.text import slugify

from django.utils.text import slugify

def generate_unique_slug(instance, title):
    slug = slugify(title)
    ModelClass = instance.__class__  
    num = 1

    while ModelClass.objects.filter(slug=slug).exists():
        slug = f"{slug}-{num}"
        num += 1

    return slug