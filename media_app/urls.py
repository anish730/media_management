from django.urls import path
from . import views

urlpatterns = [
    path('', views.media_management, name='upload_files'),
    path('files/<int:file_id>/download/', views.download_file, name='download_file'),
    path('files/<int:file_id>/delete/', views.delete_file, name='delete_file'),
]
