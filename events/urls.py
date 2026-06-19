# -*- coding: utf-8 -*-
from django.urls import path
from . import views

app_name = 'events'

urlpatterns = [
    path("add/", views.add_event, name="add_event"),
    path("", views.event_list, name="event_list"),
    path('my-events/', views.my_events, name='my_events'),
    path("eventcategories/", views.manage_event_categories, name="manage_event_categories"),
    path("category/<slug:slug>/", views.category_events, name="category_events"),
    path("<slug:slug>/", views.event_details, name="event_details"),
    path('update_event/<slug:slug>/', views.update_event, name='update_event'),
    path("eventcategories/delete/<int:category_id>/", views.delete_event_category, name="delete_event_category"),
    path("eventcategories/edit/<int:category_id>/", views.edit_event_category, name="edit_event_category"),
]
