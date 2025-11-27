# ModelYourData - Code Reference Guide

## 🎯 Quick Code Reference

### Essential Commands

```bash
# Setup
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
pip install -r requirements.txt

# Database
python manage.py makemigrations
python manage.py migrate

# Run Server
python manage.py runserver

# Create Admin
python manage.py createsuperuser

# Collect Static Files
python manage.py collectstatic

# Run Tests
python manage.py test
```

### Key Code Snippets

#### 1. File Upload Handling (views.py)

```python
def upload_csv(request):
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.save(commit=False)
            uploaded_file.original_filename = request.FILES['file'].name
            uploaded_file.file_size = request.FILES['file'].size
            uploaded_file.save()
            
            # Get row and column count
            df = pd.read_csv(uploaded_file.file.path)
            uploaded_file.row_count = len(df)
            uploaded_file.column_count = len(df.columns)
            uploaded_file.save()
            
            return redirect('analysis', file_id=uploaded_file.id)
    return redirect('landing')
```

#### 2. AJAX Operation Handler (views.py)

```python
def perform_operation(request, file_id):
    uploaded_file = get_object_or_404(UploadedFile, id=file_id)
    operation = request.POST.get('operation')
    df = utils.load_csv(uploaded_file.file.path)
    
    if operation == 'regression':
        img_base64, stats = utils.perform_linear_regression(df)
    elif operation == 'clustering':
        n_clusters = int(request.POST.get('n_clusters', 3))
        img_base64, stats = utils.perform_clustering(df, n_clusters)
    # ... other operations
    
    return JsonResponse({
        'success': True,
        'image': img_base64,
        'stats': stats
    })
```

#### 3. Linear Regression (utils.py)

```python
def perform_linear_regression(df):
    numeric_cols = get_numeric_columns(df)
    x_col, y_col = numeric_cols[0], numeric_cols[1]
    
    clean_df = df[[x_col, y_col]].dropna()
    X = clean_df[x_col].values.reshape(-1, 1)
    y = clean_df[y_col].values
    
    model = LinearRegression()
    model.fit(X, y)
    y_pred = model.predict(X)
    r2 = r2_score(y, y_pred)
    
    # Create plot
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.scatter(X, y, alpha=0.6, color='#2E7D32')
    ax.plot(X, y_pred, color='#1B5E20', linewidth=2)
    
    return plot_to_base64(fig), {
        'slope': float(model.coef_[0]),
        'intercept': float(model.intercept_),
        'r_squared': float(r2)
    }
```

#### 4. Frontend AJAX (analysis.html)

```javascript
function performOperation(operation) {
    const formData = new FormData();
    formData.append('operation', operation);
    formData.append('csrfmiddlewaretoken', csrfToken);
    
    fetch(operationUrl, {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.image) {
            vizContent.innerHTML = 
                `<img src="data:image/png;base64,${data.image}">`;
        }
        displayStats(data.stats);
    });
}
```

#### 5. Model Definition (models.py)

```python
class UploadedFile(models.Model):
    file = models.FileField(upload_to='uploads/')
    original_filename = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(default=timezone.now)
    file_size = models.IntegerField(default=0)
    row_count = models.IntegerField(null=True, blank=True)
    column_count = models.IntegerField(null=True, blank=True)
    
    class Meta:
        ordering = ['-uploaded_at']
```

#### 6. Form Validation (forms.py)

```python
class CSVUploadForm(forms.ModelForm):
    class Meta:
        model = UploadedFile
        fields = ['file']
    
    def clean_file(self):
        file = self.cleaned_data.get('file')
        
        ext = os.path.splitext(file.name)[1].lower()
        if ext != '.csv':
            raise forms.ValidationError("Only CSV files allowed.")
        
        if file.size > 10 * 1024 * 1024:
            raise forms.ValidationError("Max size 10MB.")
        
        return file
```

### URL Patterns

```python
# Project URLs (modelyourdata/urls.py)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('analyzer.urls')),
]

# App URLs (analyzer/urls.py)
urlpatterns = [
    path('', views.landing_page, name='landing'),
    path('upload/', views.upload_csv, name='upload'),
    path('analysis/<int:file_id>/', views.analysis_page, name='analysis'),
    path('operation/<int:file_id>/', views.perform_operation, name='perform_operation'),
    path('download/<int:file_id>/', views.download_visualization, name='download_viz'),
]
```

### Settings Configuration

```python
# Important Settings (modelyourdata/settings.py)

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    # ... other apps
    'analyzer',  # Our app
]

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']

FILE_UPLOAD_MAX_MEMORY_SIZE = 10485760  # 10MB
```

### CSS Variables

```css
:root {
    --primary-green: #2E7D32;
    --primary-green-dark: #1B5E20;
    --primary-green-light: #43A047;
    --white: #FFFFFF;
    --shadow-md: 0 4px 6px rgba(0, 0, 0, 0.1);
}
```

## 🔍 Common Customizations

### Change Color Scheme

Edit `static/css/style.css`:
```css
:root {
    --primary-green: #YOUR_COLOR;
    --primary-green-dark: #YOUR_DARK_COLOR;
    --primary-green-light: #YOUR_LIGHT_COLOR;
}
```

### Add New Operation

1. Add function to `analyzer/utils.py`:
```python
def perform_custom_analysis(df):
    # Your analysis code
    return img_base64, stats
```

2. Add handler to `analyzer/views.py`:
```python
elif operation == 'custom':
    img_base64, stats = utils.perform_custom_analysis(df)
```

3. Add button to `templates/analyzer/analysis.html`:
```html
<button class="operation-btn" data-operation="custom">
    <span class="op-icon">🔧</span>
    <span class="op-name">Custom Analysis</span>
</button>
```

### Change File Size Limit

Edit `modelyourdata/settings.py`:
```python
FILE_UPLOAD_MAX_MEMORY_SIZE = 20971520  # 20MB
```

And `analyzer/forms.py`:
```python
if file.size > 20 * 1024 * 1024:
    raise forms.ValidationError("Max size 20MB.")
```

## 🐛 Debugging Tips

### Enable Debug Toolbar
```bash
pip install django-debug-toolbar
```

Add to `settings.py`:
```python
INSTALLED_APPS += ['debug_toolbar']
MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']
INTERNAL_IPS = ['127.0.0.1']
```

### Check Logs
```python
import logging
logger = logging.getLogger(__name__)
logger.debug("Debug message")
```

### Inspect DataFrame
```python
print(df.head())
print(df.info())
print(df.describe())
```

## 📊 Sample Data Generation

```python
import pandas as pd
import numpy as np

# Generate sample data
np.random.seed(42)
df = pd.DataFrame({
    'age': np.random.randint(20, 60, 100),
    'salary': np.random.randint(40000, 100000, 100),
    'experience': np.random.randint(0, 20, 100),
    'satisfaction': np.random.randint(1, 11, 100)
})

df.to_csv('sample_data.csv', index=False)
```

## 🚀 Deployment Checklist

- [ ] Set `DEBUG = False`
- [ ] Change `SECRET_KEY`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Set up PostgreSQL/MySQL
- [ ] Configure static files serving
- [ ] Set up HTTPS
- [ ] Configure email backend
- [ ] Set up logging
- [ ] Configure backup system
- [ ] Set up monitoring
- [ ] Configure error tracking (Sentry)
- [ ] Use environment variables
- [ ] Set up CI/CD

## 📚 Additional Resources

- Django Documentation: https://docs.djangoproject.com/
- Pandas Documentation: https://pandas.pydata.org/docs/
- Matplotlib Documentation: https://matplotlib.org/stable/contents.html
- scikit-learn Documentation: https://scikit-learn.org/stable/

---

**Note**: This is a reference guide. See README.md for full documentation.
