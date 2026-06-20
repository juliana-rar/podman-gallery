# -*- coding: utf-8 -*-
from django.urls import path
from .views import home, biografia

app_name = "core"

urlpatterns = [
    path('', home, name="home"),
    path('biography/', biografia, name="biografia"),
]
