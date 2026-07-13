from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home_urls')),
    path('accounts/', include('accounts.urls')),
    path('courses/', include('courses.urls')),
    path('ebooks/', include('ebooks.urls')),
    path('chicks/', include('chicks.urls')),
    path('membership/', include('membership.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('consultancy/', include('consultancy.urls')),
    path('blog/', include('blog.urls')),
    path('contact/', include('contact.urls')),
    path('api/', include('api_urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    try:
        import debug_toolbar
        urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]
    except ImportError:
        pass
