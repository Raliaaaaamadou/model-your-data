# ModelYourData - Project Documentation

## 📋 Complete File Structure

```
model-your-data/
│
├── analyzer/                      # Main Django Application
│   ├── migrations/
│   │   └── __init__.py
│   ├── __init__.py
│   ├── admin.py                  # Admin configuration for UploadedFile model
│   ├── apps.py                   # App configuration
│   ├── forms.py                  # CSVUploadForm for file validation
│   ├── models.py                 # UploadedFile model
│   ├── tests.py                  # Unit tests
│   ├── urls.py                   # App URL patterns
│   ├── utils.py                  # Data analysis & visualization utilities
│   └── views.py                  # View functions (landing, upload, analysis, etc.)
│
├── modelyourdata/                # Django Project Configuration
│   ├── __init__.py
│   ├── asgi.py                   # ASGI configuration
│   ├── settings.py               # Project settings
│   ├── urls.py                   # Project URL patterns
│   └── wsgi.py                   # WSGI configuration
│
├── static/                       # Static Files
│   └── css/
│       └── style.css            # Main stylesheet (green & white theme)
│
├── templates/                    # HTML Templates
│   ├── base.html                # Base template with header/footer
│   └── analyzer/
│       ├── landing.html         # Landing page with upload form
│       └── analysis.html        # Analysis page with visualizations
│
├── media/                        # Upload directory (created on first upload)
│   └── uploads/
│
├── staticfiles/                  # Collected static files (created by collectstatic)
│
├── manage.py                     # Django management script
├── requirements.txt              # Python dependencies
├── .gitignore                    # Git ignore patterns
├── README.md                     # Comprehensive documentation
├── QUICKSTART.md                 # Quick start guide
├── sample_data.csv              # Sample CSV for testing
├── setup.sh                     # Linux/Mac setup script
├── setup.bat                    # Windows setup script
├── run.sh                       # Linux/Mac run script
└── run.bat                      # Windows run script
```

## 🔧 Technical Implementation Details

### Backend Components

#### 1. Models (`analyzer/models.py`)
- **UploadedFile**: Tracks uploaded CSV files
  - Fields: file, original_filename, uploaded_at, file_size, row_count, column_count
  - Custom delete method to remove files from storage

#### 2. Forms (`analyzer/forms.py`)
- **CSVUploadForm**: Validates CSV uploads
  - File type validation (must be .csv)
  - File size validation (max 10MB)
  - Custom error messages

#### 3. Views (`analyzer/views.py`)
- **landing_page**: Displays upload form
- **upload_csv**: Handles file upload and validation
- **analysis_page**: Displays data and analysis interface
- **perform_operation**: AJAX endpoint for analytical operations
- **download_visualization**: Downloads current visualization
- **download_csv**: Downloads original CSV file

#### 4. Utilities (`analyzer/utils.py`)
Functions for data processing and visualization:
- `load_csv()`: Load CSV into DataFrame
- `get_numeric_columns()`: Extract numeric columns
- `plot_to_base64()`: Convert matplotlib plots to base64
- `generate_table_preview()`: Create HTML table
- `perform_linear_regression()`: Linear regression analysis
- `perform_clustering()`: K-Means clustering
- `plot_distribution()`: Distribution histograms
- `generate_statistical_summary()`: Descriptive statistics
- `generate_eda_report()`: Comprehensive EDA
- `save_plot_to_file()`: Save visualizations

### Frontend Components

#### 1. Templates

**base.html**
- Header with logo and navigation
- Message display system
- Footer
- Loads CSS and JavaScript

**landing.html**
- Hero section with title and description
- Drag & drop upload area
- File browser
- Features showcase grid
- JavaScript for file handling

**analysis.html**
- File information bar
- Visualization display box
- Operation panel with 6 buttons
- Statistics display
- AJAX functionality for dynamic updates
- Loading indicators

#### 2. Styling (`static/css/style.css`)
- CSS variables for consistent theming
- Green & white color palette
- Responsive grid layouts
- Smooth transitions and animations
- Modern card-based design
- Mobile-friendly breakpoints

#### 3. JavaScript (Inline in templates)
- File drag & drop handling
- AJAX requests for operations
- Dynamic content updates
- Error handling
- Loading states

### URL Routing

**Project URLs** (`modelyourdata/urls.py`)
```python
/admin/              # Admin panel
/                    # Analyzer app URLs
```

**App URLs** (`analyzer/urls.py`)
```python
/                              # Landing page
/upload/                       # Upload endpoint
/analysis/<file_id>/          # Analysis page
/operation/<file_id>/         # Perform operation (AJAX)
/download/<file_id>/          # Download visualization
/download-csv/<file_id>/      # Download CSV
```

## 🎨 Design System

### Color Palette
- **Primary Green**: #2E7D32
- **Primary Green Dark**: #1B5E20
- **Primary Green Light**: #43A047
- **Accent Green**: #66BB6A
- **Light Green**: #81C784
- **Very Light Green**: #C8E6C9
- **Pale Green**: #E8F5E9
- **White**: #FFFFFF
- **Off White**: #F5F5F5

### Typography
- Font Family: Inter, system fonts
- Base Size: 16px
- Line Height: 1.6

### Spacing System
- XS: 0.5rem
- SM: 1rem
- MD: 1.5rem
- LG: 2rem
- XL: 3rem

### Border Radius
- SM: 4px
- MD: 8px
- LG: 12px
- XL: 16px

## 📊 Data Analysis Features

### 1. Linear Regression
- Uses first two numeric columns
- Calculates R² score
- Displays scatter plot with regression line
- Returns slope, intercept, and statistics

### 2. K-Means Clustering
- Default 3 clusters (configurable)
- Standardizes features using StandardScaler
- Visualizes first two numeric columns
- Shows cluster centroids
- Returns inertia and cluster information

### 3. Distribution Analysis
- Creates histograms for all numeric columns
- Displays mean and standard deviation
- Multiple subplots for multiple variables
- Automatic grid layout

### 4. Statistical Summary
- Descriptive statistics for all columns
- Count, mean, std, min, max, quartiles
- HTML table format
- Handles numeric and categorical data

### 5. Full EDA Report
- Correlation heatmap
- Missing values analysis
- Box plots
- Distribution plots
- Scatter plots
- Comprehensive overview

## 🔒 Security Considerations

### Current Implementation (Development)
- CSRF protection enabled
- File type validation
- File size limits
- SQL injection prevention (Django ORM)

### Production Recommendations
- Change SECRET_KEY
- Set DEBUG = False
- Configure ALLOWED_HOSTS
- Enable HTTPS
- Set up proper authentication
- Implement rate limiting
- Add file scanning for malware
- Use environment variables for secrets

## 🚀 Performance Optimization

### Current Optimizations
- Base64 encoding for images (no file I/O)
- AJAX for dynamic updates (no page reload)
- Matplotlib non-interactive backend
- Efficient DataFrame operations

### Future Improvements
- Implement caching (Redis)
- Use Celery for background tasks
- Optimize large file handling
- Add pagination for large datasets
- Implement lazy loading

## 🧪 Testing

Run tests with:
```bash
python manage.py test
```

Current test coverage:
- Model creation and validation
- Basic functionality tests

Recommended additions:
- View tests
- Form validation tests
- Utility function tests
- Integration tests
- Performance tests

## 📦 Dependencies

### Core
- Django 4.2: Web framework
- Python 3.8+: Programming language

### Data Processing
- pandas: Data manipulation
- numpy: Numerical computing

### Visualization
- matplotlib: Plotting library
- seaborn: Statistical visualizations

### Machine Learning
- scikit-learn: ML algorithms

### Image Processing
- Pillow: Image handling

## 🌐 Browser Compatibility

Tested on:
- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## 📱 Responsive Design

Breakpoints:
- Desktop: > 768px
- Tablet: 481px - 768px
- Mobile: ≤ 480px

## 🔄 Workflow

1. User uploads CSV file
2. File validated and saved
3. Redirect to analysis page
4. Display data preview
5. User clicks operation button
6. AJAX request to server
7. Server processes data
8. Returns visualization as base64
9. Frontend updates display
10. User can export or try another operation

## 📈 Future Enhancements

- [ ] User authentication and profiles
- [ ] Save and share analyses
- [ ] More chart types (pie, line, area)
- [ ] Custom color schemes
- [ ] Data filtering and sorting
- [ ] Export to PDF/Excel
- [ ] Real-time collaboration
- [ ] API for programmatic access
- [ ] Dashboard with multiple datasets
- [ ] Advanced ML models

## 📞 Support & Contribution

For issues, feature requests, or contributions:
1. Check existing issues
2. Create detailed bug reports
3. Submit pull requests with tests
4. Follow code style guidelines
5. Update documentation

---

**Version**: 1.0.0  
**Last Updated**: 2025  
**License**: MIT
