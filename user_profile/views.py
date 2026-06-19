# -*- coding: utf-8 -*-

from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required

from .forms import (
    UserRegistrationForm,
    LoginForm,
    UserProfileUpdateForm,
    ProfilePictureUpdateForm
)
from .decorators import  (
    not_logged_in_required
)
from .models import Follow, User, SiteSettings, BioPhoto


@login_required(login_url='login')
def site_config(request):
    return render(request, 'user_profile/site_config.html')


@login_required(login_url='login')
def bio_manage(request):
    return render(request, 'user_profile/bio_manage.html', {
        "bio_photos": BioPhoto.objects.all(),
    })


@login_required(login_url='login')
def update_bio(request):
    settings_obj = SiteSettings.load()
    if request.method == "POST":
        settings_obj.bio_text = request.POST.get("bio_text", "")
        if request.FILES.get("bio_photo"):
            settings_obj.bio_photo = request.FILES["bio_photo"]
        if request.FILES.get("bio_video"):
            settings_obj.bio_video = request.FILES["bio_video"]
        settings_obj.save()
        messages.success(request, "Biografía actualizada")
    return redirect("user_profile:bio_manage")


@login_required(login_url='login')
def add_bio_photo(request):
    if request.method == "POST" and request.FILES.get("image"):
        BioPhoto.objects.create(
            image=request.FILES["image"],
            caption=(request.POST.get("caption") or "").strip(),
        )
        messages.success(request, "Foto añadida al contenido destacado")
    return redirect("user_profile:bio_manage")


@login_required(login_url='login')
def delete_bio_photo(request, pk):
    photo = get_object_or_404(BioPhoto, pk=pk)
    photo.delete()
    messages.success(request, "Foto eliminada")
    return redirect("user_profile:bio_manage")


@login_required(login_url='login')
def update_site_settings(request):
    settings_obj = SiteSettings.load()
    if request.method == "POST":
        site_title = (request.POST.get("site_title") or "").strip()
        if site_title:
            settings_obj.site_title = site_title
        if request.FILES.get("favicon"):
            settings_obj.favicon = request.FILES["favicon"]
        if request.FILES.get("hero_video"):
            settings_obj.hero_video = request.FILES["hero_video"]
        if request.FILES.get("home_logo"):
            settings_obj.home_logo = request.FILES["home_logo"]
        nav_blogs = (request.POST.get("nav_blogs") or "").strip()
        nav_events = (request.POST.get("nav_events") or "").strip()
        nav_gallery = (request.POST.get("nav_gallery") or "").strip()
        if nav_blogs:
            settings_obj.nav_blogs = nav_blogs
        if nav_events:
            settings_obj.nav_events = nav_events
        if nav_gallery:
            settings_obj.nav_gallery = nav_gallery
        accent_color = (request.POST.get("accent_color") or "").strip()
        if accent_color:
            settings_obj.accent_color = accent_color
        settings_obj.instagram_url = (request.POST.get("instagram_url") or "").strip()
        settings_obj.tiktok_url = (request.POST.get("tiktok_url") or "").strip()
        settings_obj.save()
        messages.success(request, "Configuración actualizada")
    return redirect("user_profile:site_config")


@never_cache
@not_logged_in_required
def login_user(request):
    form = LoginForm()

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data.get('username'),
                password=form.cleaned_data.get('password')
            )
            if user:
                login(request, user)
                return redirect('blog:home')
            else:
                messages.warning(request, "Wrong credentials")

    context = {
        "form": form
    }
    return render(request, 'user_profile/login.html', context)


def logout_user(request):
    logout(request)
    return redirect('user_profile:login')


@never_cache
@not_logged_in_required
def register_user(request):
    form = UserRegistrationForm()

    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data.get('password'))
            user.save()
            messages.success(request, "Registration sucessful")
            return redirect('user_profile:login')

    context = {
        "form": form
    }
    return render(request, 'user_profile/registration.html', context)


@login_required(login_url='login')
def profile(request):
    account = get_object_or_404(User, pk=request.user.pk)
    form = UserProfileUpdateForm(instance=account)
    
    if request.method == "POST":
        if request.user.pk != account.pk:
            return redirect('user_profile:home')
        
        form = UserProfileUpdateForm(request.POST, instance=account)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile has been updated sucessfully")
            return redirect('user_profile:profile')
        else:
            print(form.errors)

    context = {
        "account": account,
        "form": form
    }
    return render(request, 'user_profile/profile.html', context)


@login_required
def change_profile_picture(request):
    if request.method == "POST":
        
        form = ProfilePictureUpdateForm(request.POST, request.FILES)
        
        if form.is_valid():
            image = request.FILES['profile_image']
            user = get_object_or_404(User, pk=request.user.pk)
            
            if request.user.pk != user.pk:
                return redirect('blog:home')

            user.profile_image = image
            user.save()
            messages.success(request, "Profile image updated successfully")

        else:
            print(form.errors)

    return redirect('user_profile:profile')


def view_user_information(request, username):
    account = get_object_or_404(User, username=username)
    following = False
    muted = None

    if request.user.is_authenticated:
        
        if request.user.id == account.id:
            return redirect("user_profile:profile")

        followers = account.followers.filter(
        followed_by__id=request.user.id
        )
        if followers.exists():
            following = True
    
    if following:
        queryset = followers.first()
        if queryset.muted:
            muted = True
        else:
            muted = False

    context = {
        "account": account,
        "following": following,
        "muted": muted
    }
    return render(request, "user_profile/user_information.html", context)


