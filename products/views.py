# -*- coding: utf-8 -*-
import logging

from django.shortcuts import render, get_object_or_404, redirect
from .models import Product
from .forms import ProductForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.http import JsonResponse

logger = logging.getLogger(__name__)


def product_list(request):
    queryset = Product.objects.order_by('order', '-id')
    page = request.GET.get('page', 1)
    paginator = Paginator(queryset, 24)

    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    context = {
        "products": products,
        "page_obj": products,
        "paginator": paginator,
    }
    return render(request, "products/list.html", context)


def product_details(request, slug):
    product = get_object_or_404(Product, slug=slug)
    context = {
        "product": product,
    }
    return render(request, 'products/details.html', context)


@login_required(login_url="user_profile:login")
def add_product(request):
    form = ProductForm()

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.user = request.user
            if not product.slug:
                from products.slugs import generate_unique_slug
                product.slug = generate_unique_slug(product, product.title)
            product.save()
            messages.success(request, "Producto creado correctamente")
            return redirect("products:my_products")
        else:
            logger.warning("ProductForm invalid: %s", form.errors)

    context = {
        "form": form,
    }
    return render(request, "products/add.html", context)


@login_required(login_url="user_profile:login")
def update_product(request, slug):
    product = get_object_or_404(Product, slug=slug)
    if request.user != product.user:
        return redirect("products:product_list")

    form = ProductForm(instance=product)

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            product = form.save(commit=False)
            product.user = request.user
            if not product.slug:
                from products.slugs import generate_unique_slug
                product.slug = generate_unique_slug(product, product.title)
            product.save()
            messages.success(request, "Producto actualizado correctamente")
            return redirect("products:product_list")
        else:
            logger.warning("ProductForm invalid: %s", form.errors)

    context = {
        "form": form,
        "product": product,
    }
    return render(request, "products/update.html", context)


@login_required(login_url='user_profile:login')
def my_products(request):
    delete = request.GET.get('delete')
    if delete:
        product = get_object_or_404(Product, pk=delete)
        if request.user.pk != product.user.pk:
            return redirect('home')
        product.delete()
        messages.success(request, "Tu producto ha sido eliminado!")
        return redirect('products:my_products')

    # Sin paginar: así el arrastre reordena todos los productos a la vez.
    products = request.user.user_products.all().order_by('order', '-id')

    context = {
        "products": products,
    }
    return render(request, 'products/mine.html', context)


@login_required(login_url='user_profile:login')
def update_products_hero(request):
    """Guarda la imagen y el texto del hero de la página pública de productos."""
    from user_profile.models import SiteSettings
    settings_obj = SiteSettings.load()
    if request.method == "POST":
        if request.FILES.get("products_hero_image"):
            settings_obj.products_hero_image = request.FILES["products_hero_image"]
        settings_obj.products_hero_text = request.POST.get("products_hero_text", "")
        settings_obj.products_hero_text_en = request.POST.get("products_hero_text_en", "")
        if request.FILES.get("products_hero2_image"):
            settings_obj.products_hero2_image = request.FILES["products_hero2_image"]
        settings_obj.products_hero2_text = request.POST.get("products_hero2_text", "")
        settings_obj.products_hero2_text_en = request.POST.get("products_hero2_text_en", "")
        settings_obj.save()
        messages.success(request, "Hero de productos actualizado")
    return redirect("products:my_products")


@login_required(login_url='user_profile:login')
def reorder_products(request):
    """Guarda el nuevo orden (lista de IDs) de los productos. Solo afecta a los del propio usuario."""
    if request.method != "POST":
        return JsonResponse({"ok": False}, status=405)

    ids = [i for i in (request.POST.get("order", "").split(",")) if i]
    for index, p_id in enumerate(ids):
        Product.objects.filter(pk=p_id, user=request.user).update(order=index)
    return JsonResponse({"ok": True, "count": len(ids)})
