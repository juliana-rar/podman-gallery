# -*- coding: utf-8 -*-
from django.db import models
from django.utils.text import slugify
from ckeditor.fields import RichTextField
from .slugs import generate_unique_slug
from user_profile.models import User

class MiscellanyCategory(models.Model):
    title = models.CharField(max_length=150)
    title_en = models.CharField("Title (EN)", max_length=150, blank=True)
    slug = models.SlugField(null=True, blank=True)
    created_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title

    def save(self,*args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

class Miscellany(models.Model):
    user = models.ForeignKey(
        User,
        related_name='user_miscellany',
        on_delete=models.CASCADE
    )
    category = models.ForeignKey(
        MiscellanyCategory,
        related_name='category_miscellany',
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=250)
    title_en = models.CharField("Title (EN)", max_length=250, blank=True)
    slug = models.SlugField(null=True, blank=True)
    image = models.ImageField(upload_to='event_banners/', blank=True, null=True)
    video = models.FileField("Vídeo", upload_to='event_videos/', blank=True, null=True,
                             help_text="Archivo de vídeo (.mp4). Si lo subes, se muestra en lugar de la imagen.")
    description = RichTextField(blank=True)
    description_en = RichTextField("Description (EN)", blank=True)
    order = models.PositiveIntegerField("Orden", default=0)

    class Meta:
        ordering = ['order', '-id']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            from miscellany.slugs import generate_unique_slug
            self.slug = generate_unique_slug(self, self.title)
        super().save(*args, **kwargs)
