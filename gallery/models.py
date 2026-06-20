# -*- coding: utf-8 -*-
from django.db import models
from django.utils.text import slugify

from user_profile.models import User
from .slugs import generate_unique_slug


class GalleryCategory(models.Model):
    title = models.CharField(max_length=150)
    title_en = models.CharField("Title (EN)", max_length=150, blank=True)
    slug = models.SlugField(null=True, blank=True)
    created_date = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Gallery categories"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class GalleryImage(models.Model):
    user = models.ForeignKey(
        User,
        related_name='user_gallery',
        on_delete=models.CASCADE
    )
    category = models.ForeignKey(
        GalleryCategory,
        related_name='category_gallery',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    title = models.CharField(max_length=250)
    title_en = models.CharField("Title (EN)", max_length=250, blank=True)
    slug = models.SlugField(null=True, blank=True)
    image = models.ImageField(upload_to='gallery_images/')
    description = models.TextField(blank=True)
    description_en = models.TextField("Description (EN)", blank=True)

    # Ficha técnica de la obra
    technique = models.CharField("Técnica", max_length=150, blank=True,
                                 help_text="Ej. Óleo sobre lienzo")
    technique_en = models.CharField("Technique (EN)", max_length=150, blank=True)
    paper_size = models.CharField("Tamaño de papel", max_length=100, blank=True,
                                  help_text="Ej. A3 (29,7 × 42 cm)")
    paper_size_en = models.CharField("Paper size (EN)", max_length=100, blank=True)
    dimensions = models.CharField("Dimensiones", max_length=100, blank=True,
                                  help_text="Ej. 100 × 80 cm")
    dimensions_en = models.CharField("Dimensions (EN)", max_length=100, blank=True)
    year = models.CharField("Año", max_length=10, blank=True)
    available = models.BooleanField("Disponible", default=True)
    is_premium = models.BooleanField("Premium", default=False)
    is_public = models.BooleanField("Visible en la galería", default=True,
                                    help_text="Si se desactiva, la obra no aparece en /gallery")
    is_featured = models.BooleanField("Contenido destacado", default=False,
                                      help_text="Si se activa, la obra aparece en el carrusel destacado de /biografia")
    price = models.DecimalField("Precio (€)", max_digits=10, decimal_places=2,
                                null=True, blank=True)

    order = models.PositiveIntegerField("Orden", default=0)
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', '-created_date']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug(self, self.title)
        super().save(*args, **kwargs)
