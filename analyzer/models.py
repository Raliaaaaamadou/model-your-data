"""
Models for the analyzer app.
Handles uploaded CSV files and their metadata.
"""
from django.db import models
from django.utils import timezone
import os


class UploadedFile(models.Model):
    """
    Model to track uploaded CSV files and their processing status.
    """
    file = models.FileField(upload_to='uploads/')
    original_filename = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(default=timezone.now)
    file_size = models.IntegerField(default=0)  # Size in bytes
    row_count = models.IntegerField(null=True, blank=True)
    column_count = models.IntegerField(null=True, blank=True)
    
    class Meta:
        ordering = ['-uploaded_at']
    
    def __str__(self):
        return f"{self.original_filename} - {self.uploaded_at.strftime('%Y-%m-%d %H:%M')}"
    
    def delete(self, *args, **kwargs):
        """
        Delete the file from storage when the model instance is deleted.
        """
        if self.file and os.path.isfile(self.file.path):
            os.remove(self.file.path)
        super().delete(*args, **kwargs)
