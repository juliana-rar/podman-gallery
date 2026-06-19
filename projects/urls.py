# -*- coding: utf-8 -*-
from django.urls import path, include
from .views import *
from . import views
from rest_framework.routers import DefaultRouter
from .views import ProyectoViewSet

router = DefaultRouter()
router.register(r'proyectos', ProyectoViewSet)
app_name = "projects"
urlpatterns = [
    path('api/', include(router.urls)), 
    path('api/ideas/nueva/', views.crear_idea, name='crear_idea'),
    path('proyectos/top/', views.dashboard_proyectos, name='top_proyectos'),
    path('ideas/mejorar/<int:pk>/', views.idea_mejorar_view, name='idea_mejorar'),
    path('api/mejorar-descripcion/', views.mejorar_descripcion, name='mejorar_descripcion')
]

