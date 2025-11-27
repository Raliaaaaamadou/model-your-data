# ModelYourData

A Django-based web application for CSV data visualization and analysis. Upload your CSV files and perform various analytical operations including linear regression, clustering, distribution analysis, and comprehensive exploratory data analysis (EDA).

![ModelYourData](https://img.shields.io/badge/Django-4.2-green)
![Python](https://img.shields.io/badge/Python-3.8+-blue)
![License](https://img.shields.io/badge/License-MIT-yellow)

## Features

- **CSV File Upload**: Drag & drop or browse to upload CSV files (up to 10MB)
- **Data Preview**: View your data in an interactive table
- **Linear Regression**: Analyze relationships between numeric variables
- **K-Means Clustering**: Discover patterns in your data
- **Distribution Plots**: Visualize data distributions with histograms
- **Statistical Summary**: Get comprehensive statistical insights
- **Full EDA Report**: Complete exploratory data analysis with multiple visualizations
- **Export Visualizations**: Download generated plots as PNG files
- **Responsive Design**: Works seamlessly on desktop and mobile devices
- **Modern UI**: Clean green & white theme with professional aesthetics

## Tech Stack

- **Backend**: Django 4.2
- **Data Processing**: Pandas, NumPy
- **Visualization**: Matplotlib, Seaborn
- **Machine Learning**: scikit-learn
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Database**: SQLite (default)

## Project Structure

```
model-your-data/
├── analyzer/                  # Main Django app
│   ├── __init__.py
│   ├── admin.py              # Admin interface configuration
│   ├── apps.py               # App configuration
│   ├── forms.py              # CSV upload form
│   ├── models.py             # Database models
│   ├── urls.py               # App URL routing
│   ├── utils.py              # Data analysis utilities
│   └── views.py              # View functions
├── modelyourdata/            # Django project settings
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py           # Project settings
│   ├── urls.py               # Project URL routing
│   └── wsgi.py
├── static/                   # Static files
│   └── css/
│       └── style.css         # Main stylesheet
├── templates/                # HTML templates
│   ├── base.html             # Base template
│   └── analyzer/
│       ├── landing.html      # Landing page
│       └── analysis.html     # Analysis page
├── media/                    # Uploaded files (created automatically)
├── manage.py                 # Django management script
├── requirements.txt          # Python dependencies
├── .gitignore
└── README.md
```

## Installation & Setup

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### Step-by-Step Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd model-your-data
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**
   - On Linux/Mac:
     ```bash
     source venv/bin/activate
     ```
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Apply database migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create a superuser (optional, for admin access)**
   ```bash
   python manage.py createsuperuser
   ```
   Follow the prompts to create an admin account.

7. **Create necessary directories**
   ```bash
   mkdir -p media/uploads
   mkdir -p staticfiles
   ```

8. **Collect static files**
   ```bash
   python manage.py collectstatic --noinput
   ```

## Running the Application

1. **Start the development server**
   ```bash
   python manage.py runserver
   ```

2. **Access the application**
   Open your web browser and navigate to:
   ```
   http://127.0.0.1:8000/
   ```

3. **Access the admin panel (optional)**
   Navigate to:
   ```
   http://127.0.0.1:8000/admin/
   ```
   Login with the superuser credentials you created.

## Usage Guide

### 1. Upload CSV File

- Navigate to the landing page
- Either drag & drop your CSV file or click "Browse Files" to select
- Click "Upload & Analyze" to proceed

### 2. Perform Analysis

Once uploaded, you'll be redirected to the analysis page where you can:

- **Data Preview**: View the first 20 rows of your dataset
- **Linear Regression**: Analyze the relationship between the first two numeric columns
- **Clustering**: Apply K-Means clustering (default: 3 clusters)
- **Distribution Plot**: View histograms for all numeric columns
- **Statistical Summary**: See descriptive statistics for all columns
- **Full EDA Report**: Generate a comprehensive analysis including:
  - Correlation matrix
  - Missing values analysis
  - Box plots
  - Distribution plots
  - Scatter plots

### 3. Export Results

- Click the "Export Visualization" button to download the current plot as PNG
- Click "Download CSV" to download the original file

## Sample CSV File

Create a sample CSV file to test the application:

```csv
age,salary,experience,satisfaction
25,50000,2,7
30,65000,5,8
35,80000,8,9
28,55000,3,6
42,95000,15,8
33,70000,7,7
29,60000,4,8
38,85000,10,9
```

Save this as `sample_data.csv` and upload it to the application.

## API Endpoints

- `GET /` - Landing page
- `POST /upload/` - Upload CSV file
- `GET /analysis/<file_id>/` - Analysis page
- `POST /operation/<file_id>/` - Perform analytical operation (AJAX)
- `GET /download/<file_id>/` - Download visualization
- `GET /download-csv/<file_id>/` - Download original CSV

## Configuration

### Settings

Edit `modelyourdata/settings.py` to configure:

- **Database**: Change from SQLite to PostgreSQL/MySQL for production
- **Secret Key**: Generate a new secret key for production
- **Debug**: Set `DEBUG = False` in production
- **Allowed Hosts**: Add your domain names
- **File Upload Limits**: Modify `FILE_UPLOAD_MAX_MEMORY_SIZE`

### Styling

Modify `static/css/style.css` to customize:

- Color scheme (CSS variables at the top)
- Layout and spacing
- Responsive breakpoints

## Troubleshooting

### Common Issues

1. **Import errors**
   - Ensure all dependencies are installed: `pip install -r requirements.txt`

2. **Database errors**
   - Run migrations: `python manage.py migrate`
   - Delete `db.sqlite3` and run migrations again

3. **Static files not loading**
   - Run: `python manage.py collectstatic`
   - Check `STATIC_URL` and `STATIC_ROOT` in settings

4. **File upload errors**
   - Ensure `media/uploads` directory exists
   - Check file size limits in settings

5. **Visualization not displaying**
   - Check browser console for JavaScript errors
   - Ensure CSV has numeric columns for certain operations

## Development

### Running Tests

```bash
python manage.py test
```

### Code Style

This project follows PEP 8 style guidelines. Format code with:

```bash
pip install black
black .
```

## Production Deployment

For production deployment:

1. Set `DEBUG = False` in settings
2. Configure proper database (PostgreSQL recommended)
3. Set up static file serving (WhiteNoise or CDN)
4. Use environment variables for sensitive settings
5. Enable HTTPS
6. Set up proper logging
7. Use a production WSGI server (Gunicorn, uWSGI)

Example with Gunicorn:

```bash
pip install gunicorn
gunicorn modelyourdata.wsgi:application --bind 0.0.0.0:8000
```

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## License

This project is licensed under the MIT License.

## Support

For issues, questions, or suggestions:

- Open an issue on GitHub
- Contact the development team

## Acknowledgments

- Django framework
- Pandas and NumPy communities
- Matplotlib and Seaborn visualization libraries
- scikit-learn machine learning library

---

**ModelYourData** - Making data analysis accessible and beautiful.
