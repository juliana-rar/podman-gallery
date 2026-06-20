# -*- coding: utf-8 -*-
from django.urls import path
from . import views

app_name = 'miscellany'

urlpatterns = [
    path("add/", views.add_miscellany, name="add_miscellany"),
    path("", views.miscellany_list, name="miscellany_list"),
    path('my-miscellany/', views.my_miscellany, name='my_miscellany'),
    path('reorder/', views.reorder_miscellany, name='reorder_miscellany'),
    path("miscellanycategories/", views.manage_miscellany_categories, name="manage_miscellany_categories"),
    path("category/<slug:slug>/", views.category_miscellany, name="category_miscellany"),
    path("<slug:slug>/", views.miscellany_details, name="miscellany_details"),
    path('update_miscellany/<slug:slug>/', views.update_miscellany, name='update_miscellany'),
    path("miscellanycategories/delete/<int:category_id>/", views.delete_miscellany_category, name="delete_miscellany_category"),
    path("miscellanycategories/edit/<int:category_id>/", views.edit_miscellany_category, name="edit_miscellany_category"),
]
