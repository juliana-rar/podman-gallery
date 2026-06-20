# -*- coding: utf-8 -*-
from django.db import models

from user_profile.models import User


class HeroPhoto(models.Model):
    user = models.ForeignKey(
        User,
        related_name='user_herophotos',
        on_delete=models.CASCADE
    )
    title = models.CharField("Título", max_length=200, blank=True)
    title_en = models.CharField("Title (EN)", max_length=200, blank=True)
    subtitle = models.CharField("Subtítulo", max_length=300, blank=True)
    subtitle_en = models.CharField("Subtitle (EN)", max_length=300, blank=True)
    image = models.ImageField(upload_to='hero_photos/')
    order = models.PositiveIntegerField("Orden", default=0)
    is_active = models.BooleanField("Visible", default=True)
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', '-created_date']
        verbose_name = "Hero photo"
        verbose_name_plural = "Hero photos"

    def __str__(self):
        return self.title or f"Hero #{self.pk}"
