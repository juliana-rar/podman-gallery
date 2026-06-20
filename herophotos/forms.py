# -*- coding: utf-8 -*-
from django import forms
from .models import HeroPhoto


class HeroPhotoForm(forms.ModelForm):
    class Meta:
        model = HeroPhoto
        fields = ['title', 'title_en', 'subtitle', 'subtitle_en', 'image', 'order', 'is_active']
