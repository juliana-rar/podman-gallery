from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from projects.api import ProyectoViewSet

router = DefaultRouter()
router.register(r'api/proyectos', ProyectoViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls', namespace='blog')),
    path('', include('user_profile.urls', namespace='user_profile')),
    path('', include('gallery.urls', namespace='gallery')),
    path('', include('herophotos.urls', namespace='herophotos')),
    path('', include('events.urls', namespace='events')),
    path('', include('projects.urls', namespace='projects')),
    path('ckeditor/', include('ckeditor_uploader.urls')), 
    path('', include(router.urls)),
    
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




