# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import HeroPhoto
from .forms import HeroPhotoForm


@login_required(login_url='user_profile:login')
def manage(request):
    form = HeroPhotoForm()

    if request.method == "POST":
        form = HeroPhotoForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.user = request.user
            photo.save()
            messages.success(request, "Foto añadida al hero")
            return redirect("herophotos:manage")
        else:
            print(form.errors)

    context = {
        "form": form,
        "photos": HeroPhoto.objects.all(),
    }
    return render(request, "herophotos/manage.html", context)


@login_required(login_url='user_profile:login')
def toggle_photo(request, pk):
    photo = get_object_or_404(HeroPhoto, pk=pk)
    photo.is_active = not photo.is_active
    photo.save()
    return redirect("herophotos:manage")


@login_required(login_url='user_profile:login')
def delete_photo(request, pk):
    photo = get_object_or_404(HeroPhoto, pk=pk)
    photo.delete()
    messages.success(request, "Foto eliminada")
    return redirect("herophotos:manage")
