# -*- coding: utf-8 -*-
from .models import HeroPhoto


def hero_photos(request):
    """Inyecta las fotos del hero (visibles) en todos los templates."""
    return {
        "hero_photos": HeroPhoto.objects.filter(is_active=True)[:8],
    }
