# -*- coding: utf-8 -*-
from .models import GalleryImage, GalleryCategory


def gallery_context(request):
    """Inyecta las imágenes de la galería (para el carousel del home) y sus
    categorías en todos los templates."""
    return {
        "gallery_images": GalleryImage.objects.order_by('order', '-created_date')[:12],
        "gallery_categories": GalleryCategory.objects.all(),
    }
