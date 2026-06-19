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
   path('configuracion/', site_config, name='site_config'),
   path('site-settings/', update_site_settings, name='update_site_settings'),
   path('biografia/editar/', bio_manage, name='bio_manage'),
   path('biografia/guardar/', update_bio, name='update_bio'),
   path('biografia/foto/add/', add_bio_photo, name='add_bio_photo'),
   path('biografia/foto/delete/<int:pk>/', delete_bio_photo, name='delete_bio_photo'),
   path('view_user_information/<str:username>/', view_user_information, name="view_user_information"),
]
