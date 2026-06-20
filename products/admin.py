# -*- coding: utf-8 -*-
from django.contrib import admin
from django.utils.html import format_html
from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("title", "size", "technique", "user", "image_tag", "slug")
    search_fields = ("title", "description", "size", "technique")
    list_filter = ("user",)

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-width: 80px; height:auto;" />', obj.image.url)
        return ""
    image_tag.short_description = "Preview"
