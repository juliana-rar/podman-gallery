# -*- coding: utf-8 -*-

import calendar as _calendar
from datetime import date

from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Q

from .forms import (
    UserRegistrationForm,
    LoginForm,
    UserProfileUpdateForm,
    ProfilePictureUpdateForm
)
from .decorators import  (
    not_logged_in_required
)
from .models import Follow, User, SiteSettings, BioPhoto, Exhibition


@login_required(login_url='user_profile:login')
def site_config(request):
    return render(request, 'user_profile/site_config.html')


@login_required(login_url='user_profile:login')
def bio_manage(request):
    from gallery.models import GalleryImage
    featured = (GalleryImage.objects
                .filter(is_featured=True)
                .order_by('order', '-created_date'))
    return render(request, 'user_profile/bio_manage.html', {
        "featured_images": featured,
    })


@login_required(login_url='user_profile:login')
def update_bio(request):
    settings_obj = SiteSettings.load()
    if request.method == "POST":
        settings_obj.bio_text = request.POST.get("bio_text", "")
        settings_obj.bio_text_en = request.POST.get("bio_text_en", "")
        if request.FILES.get("bio_photo"):
            settings_obj.bio_photo = request.FILES["bio_photo"]
        if request.FILES.get("bio_video"):
            settings_obj.bio_video = request.FILES["bio_video"]
        settings_obj.save()
        messages.success(request, "Biografía actualizada")
    return redirect("user_profile:bio_manage")


@login_required(login_url='user_profile:login')
def add_bio_photo(request):
    if request.method == "POST" and request.FILES.get("image"):
        BioPhoto.objects.create(
            image=request.FILES["image"],
            caption=(request.POST.get("caption") or "").strip(),
        )
        messages.success(request, "Foto añadida al contenido destacado")
    return redirect("user_profile:bio_manage")


@login_required(login_url='user_profile:login')
def delete_bio_photo(request, pk):
    photo = get_object_or_404(BioPhoto, pk=pk)
    photo.delete()
    messages.success(request, "Foto eliminada")
    return redirect("user_profile:bio_manage")


# ---------- Exhibiciones ----------

MONTHS_ES = ["", "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
             "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
MONTHS_EN = ["", "January", "February", "March", "April", "May", "June",
             "July", "August", "September", "October", "November", "December"]
WEEKDAYS_ES = ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"]
WEEKDAYS_EN = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]


@login_required(login_url='user_profile:login')
def exhibitions_manage(request):
    """Panel (admin/perfil) para crear y listar exhibiciones."""
    if request.method == "POST":
        title = (request.POST.get("title") or "").strip()
        start = request.POST.get("start_date") or ""
        if title and start:
            Exhibition.objects.create(
                title=title,
                title_en=(request.POST.get("title_en") or "").strip(),
                location=(request.POST.get("location") or "").strip(),
                location_en=(request.POST.get("location_en") or "").strip(),
                start_date=start,
                end_date=(request.POST.get("end_date") or None),
                description=(request.POST.get("description") or "").strip(),
                description_en=(request.POST.get("description_en") or "").strip(),
                url=(request.POST.get("url") or "").strip(),
            )
            messages.success(request, "Exhibición añadida")
        else:
            messages.warning(request, "Faltan el título o la fecha de inicio")
        return redirect("user_profile:exhibitions_manage")

    return render(request, "user_profile/exhibitions_manage.html", {
        "exhibitions": Exhibition.objects.all(),
        "today": timezone.localdate(),
    })


@login_required(login_url='user_profile:login')
def edit_exhibition(request, pk):
    ex = get_object_or_404(Exhibition, pk=pk)
    if request.method == "POST":
        title = (request.POST.get("title") or "").strip()
        start = request.POST.get("start_date")
        if title:
            ex.title = title
        if start:
            ex.start_date = start
        ex.title_en = (request.POST.get("title_en") or "").strip()
        ex.location = (request.POST.get("location") or "").strip()
        ex.location_en = (request.POST.get("location_en") or "").strip()
        ex.end_date = (request.POST.get("end_date") or None)
        ex.description = (request.POST.get("description") or "").strip()
        ex.description_en = (request.POST.get("description_en") or "").strip()
        ex.url = (request.POST.get("url") or "").strip()
        ex.save()
        messages.success(request, "Exhibición actualizada")
    return redirect("user_profile:exhibitions_manage")


@login_required(login_url='user_profile:login')
def delete_exhibition(request, pk):
    get_object_or_404(Exhibition, pk=pk).delete()
    messages.success(request, "Exhibición eliminada")
    return redirect("user_profile:exhibitions_manage")


def exhibitions_calendar(request):
    """Calendario público con las próximas exhibiciones."""
    today = timezone.localdate()
    try:
        year = int(request.GET.get("year", today.year))
        month = int(request.GET.get("month", today.month))
    except (TypeError, ValueError):
        year, month = today.year, today.month
    if not 1 <= month <= 12:
        year, month = today.year, today.month

    cal = _calendar.Calendar(firstweekday=0)  # semana empieza en lunes
    month_weeks = cal.monthdatescalendar(year, month)
    first_day, last_day = month_weeks[0][0], month_weeks[-1][-1]

    exhibitions = Exhibition.objects.filter(start_date__lte=last_day).filter(
        Q(end_date__gte=first_day) | Q(end_date__isnull=True, start_date__gte=first_day)
    )

    weeks = []
    for week in month_weeks:
        row = []
        for d in week:
            row.append({
                "date": d,
                "day": d.day,
                "in_month": d.month == month,
                "is_today": d == today,
                "items": [e for e in exhibitions if e.start_date <= d <= e.last_day],
            })
        weeks.append(row)

    upcoming = Exhibition.objects.filter(
        Q(end_date__gte=today) | Q(end_date__isnull=True, start_date__gte=today)
    ).order_by("start_date")[:12]

    prev_year, prev_month = (year - 1, 12) if month == 1 else (year, month - 1)
    next_year, next_month = (year + 1, 1) if month == 12 else (year, month + 1)

    return render(request, "user_profile/exhibitions.html", {
        "weeks": weeks,
        "upcoming": upcoming,
        "year": year,
        "month": month,
        "month_name": MONTHS_ES[month],
        "month_name_en": MONTHS_EN[month],
        "weekdays": [{"es": es, "en": en} for es, en in zip(WEEKDAYS_ES, WEEKDAYS_EN)],
        "prev_year": prev_year, "prev_month": prev_month,
        "next_year": next_year, "next_month": next_month,
        "today": today,
    })


@login_required(login_url='user_profile:login')
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
        if request.FILES.get("footer_signature"):
            settings_obj.footer_signature = request.FILES["footer_signature"]
        settings_obj.hero_text = request.POST.get("hero_text", "")
        settings_obj.hero_text_en = request.POST.get("hero_text_en", "")
        nav_blogs = (request.POST.get("nav_blogs") or "").strip()
        nav_miscellany = (request.POST.get("nav_miscellany") or "").strip()
        nav_gallery = (request.POST.get("nav_gallery") or "").strip()
        if nav_blogs:
            settings_obj.nav_blogs = nav_blogs
        if nav_miscellany:
            settings_obj.nav_miscellany = nav_miscellany
        if nav_gallery:
            settings_obj.nav_gallery = nav_gallery
        # English menu labels (optional; fall back to the hardcoded English in the menu)
        settings_obj.nav_blogs_en = (request.POST.get("nav_blogs_en") or "").strip()
        settings_obj.nav_miscellany_en = (request.POST.get("nav_miscellany_en") or "").strip()
        settings_obj.nav_gallery_en = (request.POST.get("nav_gallery_en") or "").strip()
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
                return redirect('core:home')
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


@login_required(login_url='user_profile:login')
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
                return redirect('core:home')

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


