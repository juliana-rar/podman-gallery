# -*- coding: utf-8 -*-
from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path("add/", views.add_product, name="add_product"),
    path("", views.product_list, name="product_list"),
    path('my-products/', views.my_products, name='my_products'),
    path('reorder/', views.reorder_products, name='reorder_products'),
    path('hero/', views.update_products_hero, name='update_products_hero'),
    path('update/<slug:slug>/', views.update_product, name='update_product'),
    path("<slug:slug>/", views.product_details, name="product_details"),
]
