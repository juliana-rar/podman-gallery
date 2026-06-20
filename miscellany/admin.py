# -*- coding: utf-8 -*-
from django.contrib import admin
from django.utils.html import format_html
from .models import Miscellany, MiscellanyCategory


@admin.register(Miscellany)
class MiscellanyAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "user", "image_tag", "slug")
    search_fields = ("title", "description")
    list_filter = ("category", "user")

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-width: 80px; height:auto;" />', obj.image.url)
        return ""
    image_tag.short_description = "Preview"


@admin.register(MiscellanyCategory)
class MiscellanyCategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "created_date")
    search_fields = ("title",)
