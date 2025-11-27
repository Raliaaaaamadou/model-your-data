# ModelYourData - Docker Guide

## 🐳 Running with Docker

### Quick Start

**Using Docker Compose (Recommended):**
```bash
docker-compose up --build
```

**Using Docker only:**
```bash
# Build the image
docker build -t modelyourdata .

# Run the container
docker run -p 8000:8000 -v $(pwd)/media:/app/media modelyourdata
```

Then open: http://localhost:8000/

### Docker Commands

**Build the image:**
```bash
docker-compose build
```

**Start the application:**
```bash
docker-compose up
```

**Start in detached mode:**
```bash
docker-compose up -d
```

**Stop the application:**
```bash
docker-compose down
```

**View logs:**
```bash
docker-compose logs -f
```

**Restart the application:**
```bash
docker-compose restart
```

**Remove volumes (clean slate):**
```bash
docker-compose down -v
```

### Creating Admin User in Docker

```bash
docker-compose exec web python manage.py createsuperuser
```

### Accessing the Container

```bash
docker-compose exec web bash
```

### Environment Variables

Create a `.env` file in the project root:

```env
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
```

Then update `docker-compose.yml` to use it:
```yaml
env_file:
  - .env
```

### Production Deployment

For production, create `docker-compose.prod.yml`:

```yaml
version: '3.8'

services:
  web:
    build: .
    command: gunicorn modelyourdata.wsgi:application --bind 0.0.0.0:8000
    volumes:
      - media_volume:/app/media
      - static_volume:/app/staticfiles
    ports:
      - "8000:8000"
    environment:
      - DEBUG=False
      - SECRET_KEY=${SECRET_KEY}
      - ALLOWED_HOSTS=${ALLOWED_HOSTS}
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - static_volume:/app/staticfiles
      - media_volume:/app/media
    ports:
      - "80:80"
    depends_on:
      - web
    restart: unless-stopped

volumes:
  media_volume:
  static_volume:
```

Run with:
```bash
docker-compose -f docker-compose.prod.yml up -d
```

### Troubleshooting

**Port already in use:**
```bash
# Change port in docker-compose.yml
ports:
  - "8001:8000"  # Use 8001 instead
```

**Permission errors:**
```bash
sudo chown -R $USER:$USER media staticfiles
```

**Container won't start:**
```bash
# Check logs
docker-compose logs web

# Rebuild from scratch
docker-compose down -v
docker-compose build --no-cache
docker-compose up
```

### Docker Image Size

The image is optimized using:
- Python slim base image
- Multi-stage builds (if needed)
- .dockerignore to exclude unnecessary files
- Cleaning apt cache

Current size: ~400-500MB

### Notes

- SQLite database is stored in the container by default
- For production, consider using PostgreSQL
- Media files are stored in Docker volumes
- Static files are collected during build
- The container runs migrations automatically on startup

### Health Check

Add to `docker-compose.yml`:
```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:8000/"]
  interval: 30s
  timeout: 10s
  retries: 3
```
