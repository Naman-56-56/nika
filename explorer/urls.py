from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('upload-csv/', views.upload_csv, name='upload_csv'),
    path('upload-image/', views.upload_image, name='upload_image'),
    path('download-report/', views.download_report, name='download_report'),
    path('download-image-report/', views.download_image_report, name='download_image_report'),
]