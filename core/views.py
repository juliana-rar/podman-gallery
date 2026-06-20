# -*- coding: utf-8 -*-
from django.shortcuts import render


def home(request):
    return render(request, 'home.html')


def biografia(request):
    from gallery.models import GalleryImage
    featured_photos = (GalleryImage.objects
                       .filter(is_featured=True, is_public=True)
                       .order_by('order', '-created_date'))
    return render(request, 'biografia.html', {"featured_photos": featured_photos})
