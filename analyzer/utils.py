"""
Utility functions for data analysis and visualization.
Handles all analytical operations: regression, clustering, EDA, plotting, etc.
"""
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from io import BytesIO
import base64
import os


# Set style for all plots
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (10, 6)
plt.rcParams['figure.dpi'] = 100


def load_csv(file_path):
    """
    Load CSV file into a pandas DataFrame.
    
    Args:
        file_path: Path to the CSV file
    
    Returns:
        DataFrame or None if error
    """
    try:
        df = pd.read_csv(file_path)
        return df
    except Exception as e:
        print(f"Error loading CSV: {e}")
        return None


def get_numeric_columns(df):
    """
    Get list of numeric columns from DataFrame.
    
    Args:
        df: pandas DataFrame
    
    Returns:
        List of numeric column names
    """
    return df.select_dtypes(include=[np.number]).columns.tolist()


def plot_to_base64(fig):
    """
    Convert matplotlib figure to base64 encoded string.
    
    Args:
        fig: matplotlib figure object
    
    Returns:
        Base64 encoded string of the image
    """
    buffer = BytesIO()
    fig.savefig(buffer, format='png', bbox_inches='tight', facecolor='white')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    plt.close(fig)
    
    graphic = base64.b64encode(image_png)
    return graphic.decode('utf-8')


def generate_table_preview(df, max_rows=10):
    """
    Generate HTML table preview of the DataFrame.
    
    Args:
        df: pandas DataFrame
        max_rows: Maximum number of rows to display
    
    Returns:
        HTML string of the table
    """
    preview_df = df.head(max_rows)
    html = preview_df.to_html(classes='data-table', index=False, border=0)
    return html


def perform_linear_regression(df):
    """
    Perform linear regression on the first two numeric columns.
    Creates scatter plot with regression line.
    
    Args:
        df: pandas DataFrame
    
    Returns:
        Tuple of (base64 image, statistics dict)
    """
    numeric_cols = get_numeric_columns(df)
    
    if len(numeric_cols) < 2:
        return None, {"error": "Need at least 2 numeric columns for regression"}
    
    # Use first two numeric columns
    x_col = numeric_cols[0]
    y_col = numeric_cols[1]
    
    # Remove NaN values
    clean_df = df[[x_col, y_col]].dropna()
    
    if len(clean_df) < 2:
        return None, {"error": "Not enough valid data points"}
    
    X = clean_df[x_col].values.reshape(-1, 1)
    y = clean_df[y_col].values
    
    # Fit linear regression
    model = LinearRegression()
    model.fit(X, y)
    
    # Make predictions
    y_pred = model.predict(X)
    
    # Calculate R-squared
    from sklearn.metrics import r2_score
    r2 = r2_score(y, y_pred)
    
    # Create plot
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.scatter(X, y, alpha=0.6, s=50, color='#2E7D32', label='Data points')
    ax.plot(X, y_pred, color='#1B5E20', linewidth=2, label=f'Regression line (R²={r2:.3f})')
    ax.set_xlabel(x_col, fontsize=12)
    ax.set_ylabel(y_col, fontsize=12)
    ax.set_title(f'Linear Regression: {y_col} vs {x_col}', fontsize=14, fontweight='bold')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # Convert to base64
    img = plot_to_base64(fig)
    
    stats = {
        "x_variable": x_col,
        "y_variable": y_col,
        "slope": float(model.coef_[0]),
        "intercept": float(model.intercept_),
        "r_squared": float(r2),
        "n_samples": len(clean_df)
    }
    
    return img, stats


def perform_clustering(df, n_clusters=3):
    """
    Perform K-Means clustering on numeric columns.
    
    Args:
        df: pandas DataFrame
        n_clusters: Number of clusters
    
    Returns:
        Tuple of (base64 image, statistics dict)
    """
    numeric_cols = get_numeric_columns(df)
    
    if len(numeric_cols) < 2:
        return None, {"error": "Need at least 2 numeric columns for clustering"}
    
    # Use only numeric columns and remove NaN
    clean_df = df[numeric_cols].dropna()
    
    if len(clean_df) < n_clusters:
        return None, {"error": f"Not enough data points for {n_clusters} clusters"}
    
    # Standardize features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(clean_df)
    
    # Perform K-Means clustering
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    clusters = kmeans.fit_predict(X_scaled)
    
    # Create visualization using first two numeric columns
    fig, ax = plt.subplots(figsize=(10, 6))
    
    scatter = ax.scatter(
        clean_df.iloc[:, 0], 
        clean_df.iloc[:, 1],
        c=clusters, 
        cmap='Greens',
        s=50, 
        alpha=0.6,
        edgecolors='black',
        linewidth=0.5
    )
    
    # Plot cluster centers (transform back to original scale)
    centers_original = scaler.inverse_transform(kmeans.cluster_centers_)
    ax.scatter(
        centers_original[:, 0],
        centers_original[:, 1],
        c='red',
        s=200,
        alpha=0.8,
        edgecolors='black',
        linewidth=2,
        marker='X',
        label='Centroids'
    )
    
    ax.set_xlabel(numeric_cols[0], fontsize=12)
    ax.set_ylabel(numeric_cols[1], fontsize=12)
    ax.set_title(f'K-Means Clustering (k={n_clusters})', fontsize=14, fontweight='bold')
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.colorbar(scatter, ax=ax, label='Cluster')
    
    img = plot_to_base64(fig)
    
    stats = {
        "n_clusters": n_clusters,
        "n_samples": len(clean_df),
        "features_used": numeric_cols[:2],
        "inertia": float(kmeans.inertia_)
    }
    
    return img, stats


def plot_distribution(df):
    """
    Create distribution plots for all numeric columns.
    
    Args:
        df: pandas DataFrame
    
    Returns:
        Tuple of (base64 image, statistics dict)
    """
    numeric_cols = get_numeric_columns(df)
    
    if len(numeric_cols) == 0:
        return None, {"error": "No numeric columns found"}
    
    # Determine subplot layout
    n_cols = min(3, len(numeric_cols))
    n_rows = (len(numeric_cols) + n_cols - 1) // n_cols
    
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(15, 5 * n_rows))
    
    # Flatten axes array for easier iteration
    if n_rows == 1 and n_cols == 1:
        axes = [axes]
    else:
        axes = axes.flatten() if n_rows > 1 or n_cols > 1 else [axes]
    
    for idx, col in enumerate(numeric_cols):
        ax = axes[idx]
        data = df[col].dropna()
        
        # Create histogram with KDE
        ax.hist(data, bins=30, alpha=0.7, color='#43A047', edgecolor='black')
        ax.set_xlabel(col, fontsize=10)
        ax.set_ylabel('Frequency', fontsize=10)
        ax.set_title(f'Distribution of {col}', fontsize=11, fontweight='bold')
        ax.grid(True, alpha=0.3)
        
        # Add statistics text
        stats_text = f'Mean: {data.mean():.2f}\nStd: {data.std():.2f}'
        ax.text(0.02, 0.98, stats_text, transform=ax.transAxes,
                verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5),
                fontsize=9)
    
    # Hide unused subplots
    for idx in range(len(numeric_cols), len(axes)):
        axes[idx].set_visible(False)
    
    plt.tight_layout()
    img = plot_to_base64(fig)
    
    stats = {
        "n_variables": len(numeric_cols),
        "variables": numeric_cols
    }
    
    return img, stats


def generate_statistical_summary(df):
    """
    Generate comprehensive statistical summary.
    
    Args:
        df: pandas DataFrame
    
    Returns:
        Tuple of (HTML table, statistics dict)
    """
    # Get descriptive statistics
    desc = df.describe(include='all').transpose()
    
    # Convert to HTML
    html = desc.to_html(classes='stats-table', border=0)
    
    stats = {
        "n_rows": len(df),
        "n_columns": len(df.columns),
        "n_numeric": len(get_numeric_columns(df)),
        "memory_usage": f"{df.memory_usage(deep=True).sum() / 1024:.2f} KB"
    }
    
    return html, stats


def generate_eda_report(df):
    """
    Generate a comprehensive EDA (Exploratory Data Analysis) report.
    Creates multiple visualizations.
    
    Args:
        df: pandas DataFrame
    
    Returns:
        Tuple of (base64 image, statistics dict)
    """
    numeric_cols = get_numeric_columns(df)
    
    if len(numeric_cols) == 0:
        return None, {"error": "No numeric columns found"}
    
    # Create figure with multiple subplots
    fig = plt.figure(figsize=(16, 12))
    gs = fig.add_gridspec(3, 2, hspace=0.3, wspace=0.3)
    
    # 1. Correlation heatmap
    ax1 = fig.add_subplot(gs[0, :])
    if len(numeric_cols) >= 2:
        corr = df[numeric_cols].corr()
        sns.heatmap(corr, annot=True, fmt='.2f', cmap='Greens', ax=ax1, 
                    cbar_kws={'label': 'Correlation'})
        ax1.set_title('Correlation Matrix', fontsize=14, fontweight='bold')
    
    # 2. Missing values
    ax2 = fig.add_subplot(gs[1, 0])
    missing = df.isnull().sum()
    missing = missing[missing > 0].sort_values(ascending=False)
    if len(missing) > 0:
        missing.plot(kind='barh', ax=ax2, color='#66BB6A')
        ax2.set_xlabel('Number of Missing Values')
        ax2.set_title('Missing Values by Column', fontsize=12, fontweight='bold')
    else:
        ax2.text(0.5, 0.5, 'No Missing Values', ha='center', va='center', fontsize=14)
        ax2.set_title('Missing Values', fontsize=12, fontweight='bold')
    
    # 3. Box plot for first numeric column
    ax3 = fig.add_subplot(gs[1, 1])
    if len(numeric_cols) > 0:
        df.boxplot(column=numeric_cols[0], ax=ax3, patch_artist=True,
                   boxprops=dict(facecolor='#81C784'))
        ax3.set_title(f'Box Plot: {numeric_cols[0]}', fontsize=12, fontweight='bold')
        ax3.set_ylabel(numeric_cols[0])
    
    # 4. Histogram for second numeric column (or first if only one)
    ax4 = fig.add_subplot(gs[2, 0])
    if len(numeric_cols) > 0:
        col_idx = 1 if len(numeric_cols) > 1 else 0
        df[numeric_cols[col_idx]].hist(bins=30, ax=ax4, color='#66BB6A', edgecolor='black')
        ax4.set_xlabel(numeric_cols[col_idx])
        ax4.set_ylabel('Frequency')
        ax4.set_title(f'Distribution: {numeric_cols[col_idx]}', fontsize=12, fontweight='bold')
    
    # 5. Scatter plot if we have at least 2 numeric columns
    ax5 = fig.add_subplot(gs[2, 1])
    if len(numeric_cols) >= 2:
        ax5.scatter(df[numeric_cols[0]], df[numeric_cols[1]], 
                   alpha=0.6, s=30, color='#43A047')
        ax5.set_xlabel(numeric_cols[0])
        ax5.set_ylabel(numeric_cols[1])
        ax5.set_title(f'{numeric_cols[1]} vs {numeric_cols[0]}', fontsize=12, fontweight='bold')
        ax5.grid(True, alpha=0.3)
    
    img = plot_to_base64(fig)
    
    stats = {
        "n_rows": len(df),
        "n_columns": len(df.columns),
        "n_numeric": len(numeric_cols),
        "missing_values": int(df.isnull().sum().sum()),
        "duplicate_rows": int(df.duplicated().sum())
    }
    
    return img, stats


def save_plot_to_file(img_base64, output_path, format='png'):
    """
    Save base64 encoded image to file.
    
    Args:
        img_base64: Base64 encoded image string
        output_path: Path where to save the file
        format: Image format (png, jpg, pdf)
    
    Returns:
        True if successful, False otherwise
    """
    try:
        import base64
        img_data = base64.b64decode(img_base64)
        with open(output_path, 'wb') as f:
            f.write(img_data)
        return True
    except Exception as e:
        print(f"Error saving plot: {e}")
        return False
