# -*- coding: utf-8 -*-
from django.contrib import admin
from django.utils.html import format_html

from .models import GalleryImage, GalleryCategory


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "technique", "paper_size", "user", "image_tag", "created_date")
    search_fields = ("title", "description", "technique", "paper_size", "dimensions")
    list_filter = ("category", "user")

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-width: 80px; height:auto;" />', obj.image.url)
        return ""
    image_tag.short_description = "Preview"


@admin.register(GalleryCategory)
class GalleryCategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "created_date")
    search_fields = ("title",)
