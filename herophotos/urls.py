# -*- coding: utf-8 -*-
from django.urls import path
from . import views

app_name = 'herophotos'

urlpatterns = [
    path("herophotos/", views.manage, name="manage"),
    path("herophotos/toggle/<int:pk>/", views.toggle_photo, name="toggle_photo"),
    path("herophotos/delete/<int:pk>/", views.delete_photo, name="delete_photo"),
]
