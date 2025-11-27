from django.contrib import admin
from .models import UploadedFile


@admin.register(UploadedFile)
class UploadedFileAdmin(admin.ModelAdmin):
    """
    Admin interface for UploadedFile model.
    """
    list_display = ['original_filename', 'uploaded_at', 'file_size', 'row_count', 'column_count']
    list_filter = ['uploaded_at']
    search_fields = ['original_filename']
    readonly_fields = ['uploaded_at', 'file_size', 'row_count', 'column_count']
