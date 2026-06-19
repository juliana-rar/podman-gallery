# -*- coding: utf-8 -*-
from django.contrib import admin
from django.utils.html import format_html

from .models import HeroPhoto


@admin.register(HeroPhoto)
class HeroPhotoAdmin(admin.ModelAdmin):
    list_display = ("__str__", "user", "order", "is_active", "image_tag", "created_date")
    list_editable = ("order", "is_active")
    list_filter = ("is_active", "user")

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-width: 120px; height:auto;" />', obj.image.url)
        return ""
    image_tag.short_description = "Preview"
