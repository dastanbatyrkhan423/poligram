"""
URL configuration for poligram_website project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from apps.core.sitemaps import StaticViewSitemap

sitemaps = {
    'static': StaticViewSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.core.urls', namespace='core')),
    path('services/', include('apps.services.urls', namespace='services')),
    # path('portfolio/', include('apps.portfolio.urls', namespace='portfolio')),  # Портфолио отключено
    path('contact/', include('apps.contact.urls', namespace='contact')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
]

# Статические файлы (только для DEBUG)
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Медиа-файлы (для DEBUG и продакшена)
# На продакшене используйте облачное хранилище (S3, Cloudinary и т.д.)
# Временно обслуживаем медиа-файлы через Django (не рекомендуется для продакшена)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
