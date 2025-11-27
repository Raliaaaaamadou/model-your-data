"""
URL configuration for the analyzer app.
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing_page, name='landing'),
    path('upload/', views.upload_csv, name='upload'),
    path('analysis/<int:file_id>/', views.analysis_page, name='analysis'),
    path('operation/<int:file_id>/', views.perform_operation, name='perform_operation'),
    path('download/<int:file_id>/', views.download_visualization, name='download_viz'),
    path('download-csv/<int:file_id>/', views.download_csv, name='download_csv'),
]
