# -*- coding: utf-8 -*-
from django import forms
from .models import Miscellany, MiscellanyCategory

class MiscellanyForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=MiscellanyCategory.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Miscellany
        fields = ['title', 'title_en', 'category', 'description', 'description_en', 'image', 'video']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Aixi nomes mostrem categories de miscellany
        self.fields['category'].queryset = MiscellanyCategory.objects.all()
