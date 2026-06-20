# -*- coding: utf-8 -*-
from django import forms
from .models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'title_en', 'size', 'technique', 'description', 'description_en', 'image']
