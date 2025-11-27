"""
Forms for the analyzer app.
Handles CSV file upload with validation.
"""
from django import forms
from .models import UploadedFile
import os


class CSVUploadForm(forms.ModelForm):
    """
    Form for uploading CSV files with validation.
    """
    class Meta:
        model = UploadedFile
        fields = ['file']
        widgets = {
            'file': forms.FileInput(attrs={
                'class': 'file-input',
                'accept': '.csv',
                'id': 'csvFile'
            })
        }
    
    def clean_file(self):
        """
        Validate the uploaded file:
        - Must be a CSV file
        - Must not exceed size limits
        """
        file = self.cleaned_data.get('file')
        
        if not file:
            raise forms.ValidationError("No file was uploaded.")
        
        # Check file extension
        ext = os.path.splitext(file.name)[1].lower()
        if ext != '.csv':
            raise forms.ValidationError("Only CSV files are allowed.")
        
        # Check file size (10MB limit)
        if file.size > 10 * 1024 * 1024:
            raise forms.ValidationError("File size must not exceed 10MB.")
        
        return file
