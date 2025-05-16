from django.urls import path
from .views import UploadView, FileDetails, landing_page, shared_files
from accounts.views import login_view

urlpatterns = [
    path('', landing_page, name='landing'),  
    path('upload/', UploadView.as_view(), name='upload'),  
    path('file/<str:file_id>/details/', FileDetails.as_view(), name='file_details'),
    path('shared/', shared_files, name='shared_files'), 
]
