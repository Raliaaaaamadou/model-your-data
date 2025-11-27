# Test models
from django.test import TestCase
from .models import UploadedFile
from django.core.files.uploadedfile import SimpleUploadedFile


class UploadedFileModelTest(TestCase):
    def test_create_uploaded_file(self):
        """Test creating an uploaded file instance"""
        csv_content = b"col1,col2\n1,2\n3,4"
        uploaded_file = SimpleUploadedFile("test.csv", csv_content, content_type="text/csv")
        
        file_obj = UploadedFile.objects.create(
            file=uploaded_file,
            original_filename="test.csv",
            file_size=len(csv_content),
            row_count=2,
            column_count=2
        )
        
        self.assertEqual(file_obj.original_filename, "test.csv")
        self.assertEqual(file_obj.row_count, 2)
        self.assertEqual(file_obj.column_count, 2)
