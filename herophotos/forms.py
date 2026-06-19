# -*- coding: utf-8 -*-
from django import forms
from .models import HeroPhoto


class HeroPhotoForm(forms.ModelForm):
    class Meta:
        model = HeroPhoto
        fields = ['title', 'subtitle', 'image', 'order', 'is_active']
