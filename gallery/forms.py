# -*- coding: utf-8 -*-
from django import forms
from .models import GalleryImage, GalleryCategory


class GalleryImageForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=GalleryCategory.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = GalleryImage
        fields = ['title', 'category', 'image', 'technique',
                  'dimensions', 'year', 'available', 'price', 'description']
