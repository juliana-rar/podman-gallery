# -*- coding: utf-8 -*-
from django import forms
from .models import Blog
from ckeditor.fields import RichTextField # type: ignore

class TextForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea, required=True)

class AddBlogForm(forms.ModelForm):
    # description = RichTextField()
    class Meta:
        model = Blog
        fields = (
            "title",
            "category",
            "banner",
            "description"
        )
        # widgets = {
        #     'description': forms.Textarea(attrs={'class': 'form-control'}),
        #     # para que tenga el mismo aspecto que todo el resto
        # }
