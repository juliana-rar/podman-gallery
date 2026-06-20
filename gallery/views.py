# -*- coding: utf-8 -*-
import logging

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.db.models import Count, Q
from django.http import JsonResponse
from django.utils.text import slugify

from .models import GalleryImage, GalleryCategory
from .forms import GalleryImageForm

logger = logging.getLogger(__name__)


def _paginate(request, queryset, per_page=12):
    paginator = Paginator(queryset, per_page)
    page = request.GET.get('page', 1)
    try:
        return paginator.page(page)
    except PageNotAnInteger:
        return paginator.page(1)
    except EmptyPage:
        return paginator.page(paginator.num_pages)


def _search(queryset, q):
    """Filtra las obras por texto: título, técnica, tamaño de papel,
    dimensiones, año, descripción y nombre de la colección."""
    if not q:
        return queryset
    return queryset.filter(
        Q(title__icontains=q)
        | Q(technique__icontains=q)
        | Q(paper_size__icontains=q)
        | Q(dimensions__icontains=q)
        | Q(year__icontains=q)
        | Q(description__icontains=q)
        | Q(category__title__icontains=q)
    ).distinct()


def _gallery_context(request, queryset, active_slug=None, category=None, mine=False):
    categories = (GalleryCategory.objects
                  .annotate(num=Count('category_gallery'))
                  .order_by('title'))
    q = (request.GET.get('q') or '').strip()
    queryset = _search(queryset, q)
    return {
        "images": _paginate(request, queryset),
        "categories": categories,
        "total_count": queryset.count(),
        "active_slug": active_slug,
        "category": category,
        "mine": mine,
        "q": q,
    }


def gallery_list(request):
    queryset = GalleryImage.objects.filter(is_public=True).order_by('order', '-created_date')
    context = _gallery_context(request, queryset)
    return render(request, "gallery/gallery.html", context)


def category_gallery(request, slug):
    category = get_object_or_404(GalleryCategory, slug=slug)
    queryset = category.category_gallery.filter(is_public=True).order_by('order', '-created_date')
    context = _gallery_context(request, queryset, active_slug=slug, category=category)
    return render(request, "gallery/gallery.html", context)


def image_details(request, slug):
    image = get_object_or_404(GalleryImage, slug=slug)
    if not image.is_public and request.user.pk != image.user_id:
        return redirect('gallery:gallery_list')
    related = (GalleryImage.objects
               .filter(category=image.category)
               .exclude(pk=image.pk)[:4]) if image.category else GalleryImage.objects.none()
    context = {"image": image, "related": related}
    return render(request, "gallery/image_details.html", context)


@login_required(login_url="user_profile:login")
def add_image(request):
    form = GalleryImageForm()
    gallery_categories = GalleryCategory.objects.all()

    if request.method == "POST":
        form = GalleryImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.user = request.user
            image.save()
            messages.success(request, "Obra publicada correctamente")
            return redirect("gallery:gallery_list")
        else:
            logger.warning("GalleryImageForm invalid: %s", form.errors)

    context = {
        "form": form,
        "gallery_categories": gallery_categories,
    }
    return render(request, "gallery/add_image.html", context)


@login_required(login_url='user_profile:login')
def my_gallery(request):
    queryset = request.user.user_gallery.all().order_by('order', '-created_date')
    delete = request.GET.get('delete')

    if delete:
        image = get_object_or_404(GalleryImage, pk=delete)
        if request.user.pk != image.user.pk:
            return redirect('gallery:gallery_list')
        image.delete()
        messages.success(request, "Obra eliminada")
        return redirect('gallery:my_gallery')

    context = _gallery_context(request, queryset, mine=True)
    return render(request, "gallery/gallery.html", context)


@login_required(login_url='user_profile:login')
def edit_image(request, pk):
    image = get_object_or_404(GalleryImage, pk=pk)
    if request.user.pk != image.user.pk:
        return redirect('gallery:image_details', slug=image.slug)

    form = GalleryImageForm(instance=image)
    gallery_categories = GalleryCategory.objects.all()

    if request.method == "POST":
        form = GalleryImageForm(request.POST, request.FILES, instance=image)
        if form.is_valid():
            form.save()
            messages.success(request, "Obra actualizada")
            return redirect('gallery:image_details', slug=image.slug)
        else:
            logger.warning("GalleryImageForm invalid: %s", form.errors)

    context = {
        "form": form,
        "image": image,
        "gallery_categories": gallery_categories,
    }
    return render(request, "gallery/edit_image.html", context)


@login_required(login_url='user_profile:login')
def reorder_gallery(request):
    """Recibe el nuevo orden de las obras (lista de IDs) y lo guarda.
    Solo afecta a obras del propio usuario."""
    if request.method != "POST":
        return JsonResponse({"ok": False}, status=405)

    ids = [i for i in (request.POST.get("order", "").split(",")) if i]
    for index, img_id in enumerate(ids):
        GalleryImage.objects.filter(pk=img_id, user=request.user).update(order=index)
    return JsonResponse({"ok": True, "count": len(ids)})


@login_required(login_url='user_profile:login')
def toggle_visibility(request, pk):
    """Muestra u oculta una obra en /gallery. Solo el dueño puede cambiarla."""
    image = get_object_or_404(GalleryImage, pk=pk)
    if request.user.pk != image.user_id:
        return redirect('gallery:gallery_list')
    image.is_public = not image.is_public
    image.save(update_fields=['is_public'])
    if image.is_public:
        messages.success(request, "«%s» ahora es visible en la galería" % image.title)
    else:
        messages.success(request, "«%s» se ocultó de la galería" % image.title)
    return redirect('gallery:my_gallery')


@login_required(login_url='user_profile:login')
def delete_image(request, pk):
    image = get_object_or_404(GalleryImage, pk=pk)
    if request.user.pk != image.user.pk:
        return redirect('gallery:image_details', slug=image.slug)
    image.delete()
    messages.success(request, "Obra eliminada")
    return redirect('gallery:gallery_list')


# ---------- Gestión de categorías (desde la propia galería) ----------

@login_required(login_url='user_profile:login')
def manage_gallery_categories(request):
    if request.method == "POST":
        title = (request.POST.get("title") or "").strip()
        if title:
            category, _ = GalleryCategory.objects.get_or_create(title=title, slug=slugify(title))
            category.title_en = (request.POST.get("title_en") or "").strip()
            category.save()
            messages.success(request, "Colección creada")
        return redirect("gallery:manage_gallery_categories")

    categories = GalleryCategory.objects.all().order_by("-created_date")
    return render(request, "gallery/manage_gallery_categories.html", {"categories": categories})


@login_required(login_url='user_profile:login')
def edit_gallery_category(request, category_id):
    category = get_object_or_404(GalleryCategory, id=category_id)
    if request.method == "POST":
        new_title = (request.POST.get("title") or "").strip()
        if new_title:
            category.title = new_title
            category.title_en = (request.POST.get("title_en") or "").strip()
            category.save()
            messages.success(request, "Colección actualizada")
    return redirect("gallery:manage_gallery_categories")


@login_required(login_url='user_profile:login')
def delete_gallery_category(request, category_id):
    category = get_object_or_404(GalleryCategory, id=category_id)
    category.delete()
    messages.success(request, "Colección eliminada")
    return redirect("gallery:manage_gallery_categories")
