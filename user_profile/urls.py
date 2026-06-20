from django.urls import path
from . import views
from .views import *

app_name = 'user_profile'

urlpatterns= [
   path('user/<str:username>/', view_user_information, name='view_user_information'),
   path('login/', login_user, name='login'),
   path('logout/', logout_user, name='logout'),
   path('register_user/', register_user, name='register_user'),
   path('profile/  ', profile, name='profile'),
   path('change_profile_picture/', change_profile_picture, name='change_profile_picture'),
   path('configuration/', site_config, name='site_config'),
   path('site-settings/', update_site_settings, name='update_site_settings'),
   path('biography/my-biography/', bio_manage, name='bio_manage'),
   path('biografia/guardar/', update_bio, name='update_bio'),
   path('biografia/foto/add/', add_bio_photo, name='add_bio_photo'),
   path('biografia/foto/delete/<int:pk>/', delete_bio_photo, name='delete_bio_photo'),
   path('exhibitions/', exhibitions_calendar, name='exhibitions'),
   path('exhibitions/my-exhibitions/', exhibitions_manage, name='exhibitions_manage'),
   path('exhibitions/hero/', update_exhibitions_hero, name='update_exhibitions_hero'),
   path('exhibiciones/editar/<int:pk>/', edit_exhibition, name='edit_exhibition'),
   path('exhibiciones/eliminar/<int:pk>/', delete_exhibition, name='delete_exhibition'),
   path('view_user_information/<str:username>/', view_user_information, name="view_user_information"),
]
