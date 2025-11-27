# ModelYourData - Quick Start Guide

## 🚀 Getting Started in 3 Steps

### Option 1: Automated Setup (Recommended)

**On Linux/Mac:**
```bash
./setup.sh
./run.sh
```

**On Windows:**
```cmd
setup.bat
run.bat
```

### Option 2: Manual Setup

1. **Install dependencies**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Setup database**
   ```bash
   python manage.py migrate
   ```

3. **Run server**
   ```bash
   python manage.py runserver
   ```

4. **Open your browser**
   ```
   http://127.0.0.1:8000/
   ```

## 📊 Try It Out

1. Upload the included `sample_data.csv` file
2. Click on different analytical operations:
   - **Data Preview**: See your data
   - **Linear Regression**: Analyze age vs salary
   - **Clustering**: Find patterns
   - **Distribution**: View data distributions
   - **Statistical Summary**: Get detailed stats
   - **Full EDA Report**: Complete analysis

3. Export your visualizations by clicking "Export Visualization"

## 🎯 Features Overview

- **Upload CSV**: Max 10MB
- **6 Analysis Types**: Preview, Regression, Clustering, Distribution, Stats, EDA
- **Interactive UI**: Click buttons to change visualizations
- **Export**: Download plots as PNG
- **Responsive**: Works on all devices

## 🛠 Troubleshooting

**Issue**: Module not found
**Fix**: `pip install -r requirements.txt`

**Issue**: Database errors
**Fix**: `python manage.py migrate`

**Issue**: Static files not loading
**Fix**: `python manage.py collectstatic`

## 📝 Next Steps

- Create admin user: `python manage.py createsuperuser`
- Access admin panel: http://127.0.0.1:8000/admin/
- Upload your own CSV files
- Explore different visualizations

## 💡 Tips

- Use CSV files with numeric columns for best results
- Try different numbers of clusters in clustering
- All visualizations update without page reload
- Export any visualization you create

---

**Need Help?** Check the full README.md for detailed documentation.
