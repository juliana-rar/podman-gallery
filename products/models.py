# -*- coding: utf-8 -*-
from django.db import models
from ckeditor.fields import RichTextField
from .slugs import generate_unique_slug
from user_profile.models import User


class Product(models.Model):
    user = models.ForeignKey(
        User,
        related_name='user_products',
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=250)
    title_en = models.CharField("Title (EN)", max_length=250, blank=True)
    slug = models.SlugField(null=True, blank=True)
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    size = models.CharField("Tamaño", max_length=150, blank=True)
    technique = models.CharField("Técnica", max_length=150, blank=True)
    description = RichTextField(blank=True)
    description_en = RichTextField("Description (EN)", blank=True)
    order = models.PositiveIntegerField("Orden", default=0)

    class Meta:
        ordering = ['order', '-id']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug(self, self.title)
        super().save(*args, **kwargs)
