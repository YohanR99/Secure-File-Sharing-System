from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static
from django.urls import include, path
from djfsender.views import landing_page, download_file, user_files

urlpatterns = [
    # Landing page
    path('', landing_page, name='landing'),

    # Admin panel
    path(f'{settings.ADMIN_PATH}/', admin.site.urls),

    # Auth-related
    path('accounts/', include('accounts.urls')),

    # App views
    path('upload/', include('djfsender.urls')),  # <-- this assumes your upload, file detail etc are in djfsender.urls

    # Dashboard & Download
    
    path('download/<str:file_id>/', download_file, name='download_file'),

    # User files
    path('my-files/', user_files, name='user_files'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
