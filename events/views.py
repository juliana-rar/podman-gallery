# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404, redirect
from .models import Event, EventCategory
from .forms import EventForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.utils.text import slugify

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def event_list(request):
    queryset = Event.objects.order_by('-id')   
    page = request.GET.get('page', 1)
    paginator = Paginator(queryset, 4)         

    try:
        events = paginator.page(page)
    except PageNotAnInteger:
        events = paginator.page(1)
    except EmptyPage:
        events = paginator.page(paginator.num_pages)  

    context = {
        "events": events,
        "page_obj": events,
        "paginator": paginator,       
    }
    return render(request, "events/events.html", context)


def category_events(request, slug):
    category = get_object_or_404(EventCategory, slug=slug)
    queryset = category.category_events.all().order_by('-id')
    page = request.GET.get('page', 1)
    paginator = Paginator(queryset, 4)

    try:
        events = paginator.page(page)
    except PageNotAnInteger:
        events = paginator.page(1)
    except EmptyPage:
        events = paginator.page(paginator.num_pages)

    context = {
        "events": events,
        "page_obj": events,
        "paginator": paginator,
        "category": category,
    }
    return render(request, "events/events.html", context)


def event_details(request, slug):
    event = get_object_or_404(Event, slug=slug)
    category = EventCategory.objects.get(id=event.category.id)

    context = {
        "event": event,
        "category": category,
        
    }
    return render(request, 'events/event_details.html', context)

@login_required(login_url="login")
def add_event(request):
    form = EventForm()
    event_categories = EventCategory.objects.all()

    if request.method == "POST":
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.user = request.user
            if not event.slug:
                from events.slugs import generate_unique_slug  
                event.slug = generate_unique_slug(event, event.title)
            event.save()
            messages.success(request, "Event creat correctament")
            return redirect("events:event_list")
        else:
            print(form.errors)



    context = {
        "form": form,
        "event_categories": event_categories,
    }
    return render(request, "events/add_event.html", context)


@login_required(login_url="login")
def update_event(request, slug):
    event = get_object_or_404(Event, slug=slug)
    if request.user != event.user:
        return redirect("events:event_list")

    form = EventForm(instance=event)
    event_categories = EventCategory.objects.all()

    if request.method == "POST":
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            event = form.save(commit=False)
            event.user = request.user
            if not event.slug:
                from events.slugs import generate_unique_slug 
                event.slug = generate_unique_slug(event, event.title)
            event.save()
            messages.success(request, "Event actualitzat correctament")
            return redirect("events:event_list")
        else:
            print(form.errors)

    context = {
        "form": form,
        "event": event,
        "event_categories": event_categories,
    }
    return render(request, "events/update_event.html", context)




@login_required(login_url='login')
def my_events(request):
    queryset = request.user.user_events.all()
    paginator = Paginator(queryset, 6)
    page = request.GET.get('page', 1)
    delete = request.GET.get('delete')
    if delete:
        event = get_object_or_404(Event, pk=delete)
        if request.user.pk != event.user.pk:
            return redirect('home')
        event.delete()
        messages.success(request, "Tu evento ha sido eliminado!")
        return redirect('events:my_events')

    try:
        events = paginator.page(page)
    except (EmptyPage, PageNotAnInteger):
        events = paginator.page(1)

    event_categories = EventCategory.objects.all().order_by('-created_date')

    context = {
        "events": events,
        "page_obj": events,
        "paginator": paginator,
        "event_categories": event_categories,  
    }

    return render(request, 'events/my_events.html', context)


def manage_event_categories(request):
    if request.method == "POST":
        title = request.POST.get("title")
        if title:
            EventCategory.objects.create(title=title, slug=slugify(title))
            return redirect("events:manage_event_categories")

    event_categories = EventCategory.objects.all().order_by("-created_date")
    return render(request, "events/manage_event_categories.html", {"event_categories": event_categories})


def delete_event_category(request, category_id):
    category = get_object_or_404(EventCategory, id=category_id)
    category.delete()
    return redirect("events:manage_event_categories")


def edit_event_category(request, category_id):
    category = get_object_or_404(EventCategory, id=category_id)
    if request.method == "POST":
        new_title = request.POST.get("title")
        if new_title:
            category.title = new_title
            category.slug = slugify(new_title)
            category.save()
        return redirect("events:manage_event_categories")  
    event_categories = EventCategory.objects.all().order_by("-created_date")
    return render(request, "events/edit_event_category.html", {"event_categories": event_categories})
