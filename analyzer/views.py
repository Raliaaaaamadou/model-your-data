"""
Views for the analyzer app.
Handles all HTTP requests and responses.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse, FileResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from .models import UploadedFile
from .forms import CSVUploadForm
from . import utils
import os
import pandas as pd
import tempfile


def landing_page(request):
    """
    Landing page with CSV upload form.
    """
    form = CSVUploadForm()
    return render(request, 'analyzer/landing.html', {'form': form})


def upload_csv(request):
    """
    Handle CSV file upload.
    Validates, saves file, and redirects to analysis page.
    """
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        
        if form.is_valid():
            # Save the uploaded file
            uploaded_file = form.save(commit=False)
            uploaded_file.original_filename = request.FILES['file'].name
            uploaded_file.file_size = request.FILES['file'].size
            uploaded_file.save()
            
            # Load CSV to get row and column count
            try:
                df = pd.read_csv(uploaded_file.file.path)
                uploaded_file.row_count = len(df)
                uploaded_file.column_count = len(df.columns)
                uploaded_file.save()
            except Exception as e:
                messages.error(request, f"Error reading CSV file: {e}")
                uploaded_file.delete()
                return redirect('landing')
            
            # Redirect to analysis page
            return redirect('analysis', file_id=uploaded_file.id)
        else:
            # Form is invalid
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)
            return redirect('landing')
    
    return redirect('landing')


def analysis_page(request, file_id):
    """
    Main analysis page displaying data preview and operations.
    """
    uploaded_file = get_object_or_404(UploadedFile, id=file_id)
    
    # Load the CSV file
    df = utils.load_csv(uploaded_file.file.path)
    
    if df is None:
        messages.error(request, "Error loading CSV file.")
        return redirect('landing')
    
    # Generate initial table preview
    table_html = utils.generate_table_preview(df, max_rows=10)
    
    # Get basic info
    numeric_cols = utils.get_numeric_columns(df)
    
    context = {
        'file': uploaded_file,
        'table_html': table_html,
        'n_rows': len(df),
        'n_columns': len(df.columns),
        'n_numeric': len(numeric_cols),
        'columns': df.columns.tolist(),
        'numeric_columns': numeric_cols,
    }
    
    return render(request, 'analyzer/analysis.html', context)


def perform_operation(request, file_id):
    """
    AJAX endpoint to perform analytical operations.
    Returns JSON response with visualization and statistics.
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method'}, status=400)
    
    uploaded_file = get_object_or_404(UploadedFile, id=file_id)
    operation = request.POST.get('operation')
    
    # Load the CSV file
    df = utils.load_csv(uploaded_file.file.path)
    
    if df is None:
        return JsonResponse({'error': 'Error loading CSV file'}, status=400)
    
    # Perform the requested operation
    img_base64 = None
    stats = {}
    html_content = None
    
    try:
        if operation == 'regression':
            img_base64, stats = utils.perform_linear_regression(df)
            
        elif operation == 'clustering':
            n_clusters = int(request.POST.get('n_clusters', 3))
            img_base64, stats = utils.perform_clustering(df, n_clusters)
            
        elif operation == 'distribution':
            img_base64, stats = utils.plot_distribution(df)
            
        elif operation == 'summary':
            html_content, stats = utils.generate_statistical_summary(df)
            
        elif operation == 'eda':
            img_base64, stats = utils.generate_eda_report(df)
            
        elif operation == 'preview':
            html_content = utils.generate_table_preview(df, max_rows=20)
            stats = {
                'n_rows': len(df),
                'n_columns': len(df.columns)
            }
        
        else:
            return JsonResponse({'error': 'Unknown operation'}, status=400)
        
        # Check for errors in stats
        if stats and 'error' in stats:
            return JsonResponse({'error': stats['error']}, status=400)
        
        # Store the current visualization in session for download
        if img_base64:
            request.session['current_viz'] = img_base64
            request.session['current_operation'] = operation
        
        response_data = {
            'success': True,
            'operation': operation,
            'stats': stats,
        }
        
        if img_base64:
            response_data['image'] = img_base64
        
        if html_content:
            response_data['html'] = html_content
        
        return JsonResponse(response_data)
    
    except Exception as e:
        return JsonResponse({'error': f'Error performing operation: {str(e)}'}, status=500)


def download_visualization(request, file_id):
    """
    Download the current visualization as PNG.
    """
    uploaded_file = get_object_or_404(UploadedFile, id=file_id)
    
    # Get the current visualization from session
    img_base64 = request.session.get('current_viz')
    operation = request.session.get('current_operation', 'visualization')
    
    if not img_base64:
        messages.error(request, "No visualization available to download.")
        return redirect('analysis', file_id=file_id)
    
    # Convert base64 to image file
    import base64
    img_data = base64.b64decode(img_base64)
    
    # Create response with image
    response = HttpResponse(img_data, content_type='image/png')
    filename = f'{uploaded_file.original_filename.rsplit(".", 1)[0]}_{operation}.png'
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    
    return response


def download_csv(request, file_id):
    """
    Download the original CSV file.
    """
    uploaded_file = get_object_or_404(UploadedFile, id=file_id)
    
    # Return the file as download
    response = FileResponse(
        open(uploaded_file.file.path, 'rb'),
        content_type='text/csv'
    )
    response['Content-Disposition'] = f'attachment; filename="{uploaded_file.original_filename}"'
    
    return response
