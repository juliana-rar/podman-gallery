# -*- coding: utf-8 -*-
from django.urls import path
from . import views

app_name = 'gallery'

urlpatterns = [
    path("gallery/", views.gallery_list, name="gallery_list"),
    path("gallery/add/", views.add_image, name="add_image"),
    path("gallery/mine/", views.my_gallery, name="my_gallery"),
    path("gallerycategories/", views.manage_gallery_categories, name="manage_gallery_categories"),
    path("gallerycategories/edit/<int:category_id>/", views.edit_gallery_category, name="edit_gallery_category"),
    path("gallerycategories/delete/<int:category_id>/", views.delete_gallery_category, name="delete_gallery_category"),
    path("gallery/reorder/", views.reorder_gallery, name="reorder_gallery"),
    path("gallery/edit/<int:pk>/", views.edit_image, name="edit_image"),
    path("gallery/delete/<int:pk>/", views.delete_image, name="delete_image"),
    path("gallery/category/<slug:slug>/", views.category_gallery, name="category_gallery"),
    path("gallery/<slug:slug>/", views.image_details, name="image_details"),
]
