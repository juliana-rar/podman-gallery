# -*- coding: utf-8 -*-
import logging

from django.shortcuts import render, get_object_or_404, redirect
from .models import Miscellany, MiscellanyCategory
from .forms import MiscellanyForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.utils.text import slugify
from django.db.models import Count
from django.http import JsonResponse

logger = logging.getLogger(__name__)

def miscellany_list(request):
    queryset = Miscellany.objects.order_by('order', '-id')
    page = request.GET.get('page', 1)
    paginator = Paginator(queryset, 24)

    try:
        events = paginator.page(page)
    except PageNotAnInteger:
        events = paginator.page(1)
    except EmptyPage:
        events = paginator.page(paginator.num_pages)

    categories = MiscellanyCategory.objects.annotate(num=Count('category_miscellany')).order_by('title')

    context = {
        "events": events,
        "page_obj": events,
        "paginator": paginator,
        "categories": categories,
    }
    return render(request, "miscellany/list.html", context)


def category_miscellany(request, slug):
    category = get_object_or_404(MiscellanyCategory, slug=slug)
    queryset = category.category_miscellany.all().order_by('order', '-id')
    page = request.GET.get('page', 1)
    paginator = Paginator(queryset, 24)

    try:
        events = paginator.page(page)
    except PageNotAnInteger:
        events = paginator.page(1)
    except EmptyPage:
        events = paginator.page(paginator.num_pages)

    categories = MiscellanyCategory.objects.annotate(num=Count('category_miscellany')).order_by('title')

    context = {
        "events": events,
        "page_obj": events,
        "paginator": paginator,
        "category": category,
        "categories": categories,
        "active_slug": category.slug,
    }
    return render(request, "miscellany/list.html", context)


def miscellany_details(request, slug):
    event = get_object_or_404(Miscellany, slug=slug)
    category = MiscellanyCategory.objects.get(id=event.category.id)

    context = {
        "event": event,
        "category": category,

    }
    return render(request, 'miscellany/details.html', context)

@login_required(login_url="user_profile:login")
def add_miscellany(request):
    form = MiscellanyForm()
    event_categories = MiscellanyCategory.objects.all()

    if request.method == "POST":
        form = MiscellanyForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.user = request.user
            if not event.slug:
                from miscellany.slugs import generate_unique_slug
                event.slug = generate_unique_slug(event, event.title)
            event.save()
            messages.success(request, "Pieza creada correctamente")
            return redirect("miscellany:my_miscellany")
        else:
            logger.warning("MiscellanyForm invalid: %s", form.errors)



    context = {
        "form": form,
        "event_categories": event_categories,
    }
    return render(request, "miscellany/add.html", context)


@login_required(login_url="user_profile:login")
def update_miscellany(request, slug):
    event = get_object_or_404(Miscellany, slug=slug)
    if request.user != event.user:
        return redirect("miscellany:miscellany_list")

    form = MiscellanyForm(instance=event)
    event_categories = MiscellanyCategory.objects.all()

    if request.method == "POST":
        form = MiscellanyForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            event = form.save(commit=False)
            event.user = request.user
            if not event.slug:
                from miscellany.slugs import generate_unique_slug
                event.slug = generate_unique_slug(event, event.title)
            event.save()
            messages.success(request, "Pieza actualizada correctamente")
            return redirect("miscellany:miscellany_list")
        else:
            logger.warning("MiscellanyForm invalid: %s", form.errors)

    context = {
        "form": form,
        "event": event,
        "event_categories": event_categories,
    }
    return render(request, "miscellany/update.html", context)




@login_required(login_url='user_profile:login')
def my_miscellany(request):
    delete = request.GET.get('delete')
    if delete:
        event = get_object_or_404(Miscellany, pk=delete)
        if request.user.pk != event.user.pk:
            return redirect('home')
        event.delete()
        messages.success(request, "Tu pieza ha sido eliminada!")
        return redirect('miscellany:my_miscellany')

    # Sin paginar: así el arrastre reordena todas las piezas a la vez.
    events = request.user.user_miscellany.all().order_by('order', '-id')
    event_categories = MiscellanyCategory.objects.all().order_by('-created_date')

    context = {
        "events": events,
        "event_categories": event_categories,
    }

    return render(request, 'miscellany/mine.html', context)


@login_required(login_url='user_profile:login')
def reorder_miscellany(request):
    """Guarda el nuevo orden (lista de IDs) de las piezas. Solo afecta a las del propio usuario."""
    if request.method != "POST":
        return JsonResponse({"ok": False}, status=405)

    ids = [i for i in (request.POST.get("order", "").split(",")) if i]
    for index, ev_id in enumerate(ids):
        Miscellany.objects.filter(pk=ev_id, user=request.user).update(order=index)
    return JsonResponse({"ok": True, "count": len(ids)})


def manage_miscellany_categories(request):
    if request.method == "POST":
        title = request.POST.get("title")
        if title:
            MiscellanyCategory.objects.create(
                title=title,
                title_en=(request.POST.get("title_en") or "").strip(),
                slug=slugify(title),
            )
            return redirect("miscellany:manage_miscellany_categories")

    event_categories = MiscellanyCategory.objects.all().order_by("-created_date")
    return render(request, "miscellany/manage_categories.html", {"event_categories": event_categories})


def delete_miscellany_category(request, category_id):
    category = get_object_or_404(MiscellanyCategory, id=category_id)
    category.delete()
    return redirect("miscellany:manage_miscellany_categories")


def edit_miscellany_category(request, category_id):
    category = get_object_or_404(MiscellanyCategory, id=category_id)
    if request.method == "POST":
        new_title = request.POST.get("title")
        if new_title:
            category.title = new_title
            category.title_en = (request.POST.get("title_en") or "").strip()
            category.slug = slugify(new_title)
            category.save()
        return redirect("miscellany:manage_miscellany_categories")
    event_categories = MiscellanyCategory.objects.all().order_by("-created_date")
    return render(request, "miscellany/edit_category.html", {"event_categories": event_categories})
