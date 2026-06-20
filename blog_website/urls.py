from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls', namespace='core')),
    path('', include('user_profile.urls', namespace='user_profile')),
    path('', include('gallery.urls', namespace='gallery')),
    path('', include('herophotos.urls', namespace='herophotos')),
    path('miscellany/', include('miscellany.urls', namespace='miscellany')),
    path('products/', include('products.urls', namespace='products')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




