# -*- coding: utf-8 -*-
from django.urls import path, include
from .views import *
from . import views

app_name = "blog"

urlpatterns = [
    path('', home, name="home"),
    path('biografia/', biografia, name="biografia"),
    path('blogs/', blogs, name="blogs"),
    path('blogs/<str:slug>/', blog_details, name='blog_details'),
    path('category_blogs/<str:slug>/', category_blogs, name='category_blogs'),
    path('tag_blogs/<str:slug>/', tag_blogs, name='tag_blogs'),  
    path('tag/<slug:slug>/', tag_blogs, name='tag_blogs'),  
    path('search/', search_blogs, name='search_blogs'),
    path('my_blogs/', my_blogs, name='my_blogs'),
    path('add_blog/', add_blog, name='add_blog'),
    path('update_blog/<str:slug>/', update_blog, name='update_blog'),
    path("blogcategories/", views.manage_categories, name="manage_categories"),
    path("blogcategories/delete/<int:category_id>/", views.delete_category, name="delete_category"),
    path("blogcategories/edit/<int:category_id>/", views.edit_category, name="edit_category"),  
    path('events/', include('events.urls', namespace='events')),
]