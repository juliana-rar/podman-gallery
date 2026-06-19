# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404, redirect, render
from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator
from django.contrib.auth.decorators import login_required
from django.utils.text import slugify
from django.contrib import messages
from .models import Blog
from django.http import JsonResponse
from django.db.models import Q
from user_profile.models import User
from events.models import Event, EventCategory
from django.shortcuts import render, get_object_or_404, redirect

from .models import (
    Blog,
    Category,
    Tag,
    Comment,
    Reply,
)
from .forms import TextForm, AddBlogForm

def home(request):
    blogs = Blog.objects.order_by('-created_date')[:4]
    events = Event.objects.order_by('-id')[:4]
    event_categories = EventCategory.objects.all()
    context = {
        "blogs" : blogs,
        "events": events,
        "event_categories": event_categories,
    }
    return render(request, 'home.html', context)

def blogs(request):
    queryset = Blog.objects.order_by('-created_date')
    tags = Tag.objects.order_by('-created_date')
    page = request.GET.get('page', 1)
    paginator = Paginator(queryset, 4)
    
    
    try:
        blogs = paginator.page(page)
    except EmptyPage:
        blogs = paginator.page(1)
    except PageNotAnInteger:
        blogs = paginator.page(1)
        return redirect('blogs')

    context = {
        "blogs" : blogs,
        "tags" : tags,
        "page_obj": blogs,
        "paginator" : paginator
    }
    return render(request, 'blogs/blogs.html', context)

def category_blogs(request, slug):
    category = get_object_or_404(Category, slug=slug)
    queryset = category.category_blogs.all()
    tags = Tag.objects.order_by("-created_date")[:5]
    page = request.GET.get('page', 1)
    paginator = Paginator(queryset, 6) 
    all_blogs = Blog.objects.order_by('-created_date')[:5]
    
    try:
        blogs = paginator.page(page)
    except EmptyPage:
        blogs = paginator.page(1)
    except PageNotAnInteger:
        blogs = paginator.page(1)
        return redirect('blogs')
    
    context = {
        "blogs": blogs,
        "tags": tags,
        "all_blogs": all_blogs,
        "category": category

    }
    return render(request, 'blogs/category_blogs.html', context)


def tag_blogs(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    queryset = tag.tag_blogs.all()
    tags = Tag.objects.order_by('-created_date')[:5]
    page = request.GET.get('page', 1)
    paginator = Paginator(queryset, 2)
    all_blogs = Blog.objects.order_by('-created_date')[:5]
    
    try:
        blogs = paginator.page(page)
    except EmptyPage:
        blogs = paginator.page(1)
    except PageNotAnInteger:
        blogs = paginator.page(1)
        return redirect('blog:blogs')
      
    context = {
        "blogs": blogs,
        "tags": tags,
        "all_blogs": all_blogs

    }
    return render(request, 'blogs/category_blogs.html', context)


def blog_details(request, slug):
    form = TextForm()
    blog = get_object_or_404(Blog, slug=slug)
    category = Category.objects.get(id=blog.category.id )
    related_blogs = category.category_blogs.all()

    tags = Tag.objects.order_by('-created_date')[:5]
    recent_posts = Blog.objects.order_by('-created_date')[:5]

    liked_by = request.user in blog.likes.all()

    if request.method == "POST" and request.user.is_authenticated:
        form = TextForm(request.POST)
        if form.is_valid():
            Comment.objects.create(
                user=request.user,
                blog=blog,
                text=form.cleaned_data.get('text')
            )
            return redirect('blog:blog_details', slug=slug)
    context = {
        "blog": blog,
        "related_blogs": related_blogs,
        "tags": tags,
        "form": form,
        "liked_by": liked_by,
        "recent_posts": recent_posts  

    }
    return render(request, 'blogs/blog_details.html', context)


@login_required(login_url="login")
def add_reply(request, blog_id, comment_id):
    blog = get_object_or_404(Blog, id=blog_id)
    if request.method == "POST":
        form = TextForm(request.POST)
        if form.is_valid(): 

            comment = get_object_or_404(Comment, id=comment_id)
            Reply.objects.create(
                user=request.user,
                comment=comment,
                text=form.cleaned_data.get('text')
            )
    return redirect('blog:blog_details', slug=blog.slug)

@login_required(login_url='login')
def like_blog(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    liked = False
    if request.user.is_authenticated:
        if request.user in blog.likes.all():
            blog.likes.remove(request.user)
        else:
            blog.likes.add(request.user)
            liked = True
    
    like_count = blog.likes.count()

    return JsonResponse({'liked': liked, 'like_count': like_count})

def search_blogs(request):
    search_key = request.GET.get('search', None)
    recent_blogs = Blog.objects.order_by('-created_date')
    tags = Tag.objects.order_by('-created_date')
    if search_key:
        blogs = Blog.objects.filter(
            Q(title__icontains=search_key) |
            Q(category__title__icontains=search_key) |
            Q(user__username__icontains=search_key) |
            Q(tags__title__icontains=search_key)
        ).distinct()

        context = {
            "blogs": blogs,
            "recent_blogs": recent_blogs,
            "tags": tags,
            "search_key": search_key

        }
        return render(request, 'search.html', context)
    else:
        return redirect('blog:home')
    




@login_required(login_url="login")
def my_blogs(request):
    queryset = request.user.user_blogs.all()
    paginator = Paginator(queryset, 6)
    page = request.GET.get('page', 1)
    delete = request.GET.get('delete', None)

    if delete:
       
        blog = get_object_or_404(Blog, pk=delete)
        if request.user.pk != blog.user.pk:
            return redirect('blog:home')
        
        blog.delete()
        messages.success(request, "your blog has been deleted!")
        return redirect('blogs:my_blogs')

    try:
        blogs = paginator.page(page)
    except EmptyPage:
        blogs = paginator.page(1)
    except PageNotAnInteger:
        blogs = paginator.page(1)
        return redirect('blogs')
    
    context = {
        "blogs": blogs,
        "page_obj": blogs,
        "paginator": paginator
    }

    return render(request, 'blogs/my_blogs.html', context)





@login_required(login_url='login')
def add_blog(request):
    form = AddBlogForm()

    if request.method == "POST":
        form = AddBlogForm(request.POST, request.FILES)
        if form.is_valid():
            tags = request.POST['tags'].split(',')
            user = get_object_or_404(User, pk=request.user.pk)
            category = get_object_or_404(Category, pk=request.POST['category'])
            blog = form.save(commit=False)
            blog.user = user
            
            blog.category = category
            blog.save()

            for tag in tags:
                tag_input = Tag.objects.filter(
                    title__iexact=tag.strip(),
                    slug=slugify(tag.strip())
                )
                if tag_input.exists():
                    t = tag_input.first()
                    blog.tags.add(t)

                else:
                    if tag != '':
                        new_tag = Tag.objects.create(
                            title = tag.strip(),
                            slug=slugify(tag.strip())
                        )
                        blog.tags.add(new_tag)


            messages.success(request, "blog addedd successfully")
            return redirect('blog:blog_details', slug=blog.slug)
        else:
            print(form.errors)

    context = {
        "form": form

    }
    return render(request, 'blogs/add_blog.html', context)

@login_required(login_url='login')
def update_blog(request, slug):
    blog = get_object_or_404(Blog, slug=slug)
    form = AddBlogForm(instance=blog)

    if request.method == "POST":
        form = AddBlogForm(request.POST, request.FILES, instance=blog)
        
        if form.is_valid():
            
            if request.user.pk != blog.user.pk:
                return redirect('blog:home')

            tags = request.POST['tags'].split(',')
            user = get_object_or_404(User, pk=request.user.pk)
            category = get_object_or_404(Category, pk=request.POST['category'])
            blog = form.save(commit=False)
            blog.user = user
            blog.category = category
            blog.save()

            for tag in tags:
                tag_input = Tag.objects.filter(
                    title__iexact=tag.strip(),
                    slug=slugify(tag.strip())
                )
                if tag_input.exists():
                    t = tag_input.first()
                    blog.tags.add(t)

                else:
                    if tag != '':
                        new_tag = Tag.objects.create(
                            title=tag.strip(),
                            slug=slugify(tag.strip())
                        )
                        blog.tags.add(new_tag)

            messages.success(request, "Blog updated successfully")
            return redirect('blog:blog_details', slug=blog.slug)
        else:
            print(form.errors)


    context = {
        "form": form,
        "blog": blog,
        'blog_categories': Category.objects.all().order_by('title')
    }
    return render(request, 'blogs/update_blog.html', context)


def manage_categories(request):
    if request.method == "POST":
        title = request.POST.get("title")
        if title:
            Category.objects.get_or_create(title=title)  
        return redirect("blog:manage_categories")

    categories = Category.objects.all().order_by("-created_date")
    return render(request, "blogs/manage_categories.html", {"categories": categories})


def edit_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    if request.method == "POST":
        new_title = request.POST.get("title")
        if new_title:
            category.title = new_title
            category.save()
            return redirect("blog:manage_categories")  # volver a la lista
    return render(request, "blogs/edit_category.html", {"category": category})

@login_required
def delete_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    category.delete()
    return redirect("blog:manage_categories")