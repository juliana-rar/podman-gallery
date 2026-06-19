# -*- coding: utf-8 -*-
from .models import SiteSettings


def site_settings(request):
    """Inyecta la configuración del sitio (nombres del menú) en todos los templates."""
    return {"site_settings": SiteSettings.load()}
