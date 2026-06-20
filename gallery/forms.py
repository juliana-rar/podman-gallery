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
        fields = ['title', 'title_en', 'category', 'image', 'technique', 'technique_en',
                  'paper_size', 'paper_size_en', 'dimensions', 'dimensions_en',
                  'year', 'available', 'is_premium', 'is_featured',
                  'price', 'description', 'description_en']
