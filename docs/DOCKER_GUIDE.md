# Docker Setup Guide for CloudFlow SaaS Platform

## 🐳 What is Docker?

Docker is like a shipping container for your application. It packages your code, database, and all dependencies into containers that can run anywhere - your computer, a server, or the cloud.

## 📁 Docker Files Explanation

### `docker/Dockerfile`
This file tells Docker how to build your application container:
- Installs Python and required system packages
- Copies your code into the container
- Sets up the environment
- Defines how to run the application

### `docker/docker-compose.yml` (Production)
This file defines multiple services working together:
- **Web**: Your Django application
- **DB**: MySQL database
- **Redis**: Caching and background tasks
- **Nginx**: Web server for handling requests
- **Celery**: Background task workers

### `docker/docker-compose.dev.yml` (Development)
Simplified version for development:
- Enables live code reloading
- Uses development settings
- Easier debugging

## 🚀 Quick Start with Docker

### Prerequisites
Install Docker on your system:
- **Windows**: Download Docker Desktop from docker.com
- **Mac**: Download Docker Desktop from docker.com
- **Linux**: Follow Docker installation guide for your distribution

### Development Setup (Recommended for Learning)

1. **Navigate to project directory:**
```bash
cd ProjectC
```

2. **Start development environment:**
```bash
# Start all services
docker-compose -f docker/docker-compose.dev.yml up --build

# Or run in background
docker-compose -f docker/docker-compose.dev.yml up --build -d
```

3. **Wait for services to start** (first time takes longer)

4. **Access your application:**
- Website: http://localhost:8000
- Database: localhost:3306 (user: saas_user, password: saas_password)
- Redis: localhost:6379

### Production Setup

1. **Configure environment variables:**
```bash
# Copy docker environment template
cp docker/.env.example docker/.env

# Edit docker/.env with your production settings:
# - Email configuration
# - Stripe keys
# - Strong passwords
# - Domain names
```

2. **Start production environment:**
```bash
docker-compose -f docker/docker-compose.yml up --build -d
```

3. **Access your application:**
- Website: http://localhost (port 80)
- Admin: http://localhost/admin/

## 🛠️ Docker Commands Reference

### Starting Services
```bash
# Start development environment
docker-compose -f docker/docker-compose.dev.yml up

# Start in background (detached)
docker-compose -f docker/docker-compose.dev.yml up -d

# Build and start (force rebuild)
docker-compose -f docker/docker-compose.dev.yml up --build

# Start only specific services
docker-compose -f docker/docker-compose.dev.yml up db redis
```

### Stopping Services
```bash
# Stop all services
docker-compose -f docker/docker-compose.dev.yml down

# Stop and remove volumes (deletes data!)
docker-compose -f docker/docker-compose.dev.yml down -v

# Stop specific service
docker-compose -f docker/docker-compose.dev.yml stop web
```

### Viewing Logs
```bash
# View all logs
docker-compose -f docker/docker-compose.dev.yml logs

# View specific service logs
docker-compose -f docker/docker-compose.dev.yml logs web

# Follow logs (live updates)
docker-compose -f docker/docker-compose.dev.yml logs -f web
```

### Accessing Containers
```bash
# Run command in container
docker-compose -f docker/docker-compose.dev.yml exec web python manage.py shell

# Open bash shell in container
docker-compose -f docker/docker-compose.dev.yml exec web bash

# Run Django management commands
docker-compose -f docker/docker-compose.dev.yml exec web python manage.py migrate
docker-compose -f docker/docker-compose.dev.yml exec web python manage.py createsuperuser
```

## 🗄️ Database Operations

### Initial Database Setup
```bash
# Create and run migrations
docker-compose -f docker/docker-compose.dev.yml exec web python manage.py makemigrations
docker-compose -f docker/docker-compose.dev.yml exec web python manage.py migrate

# Create superuser
docker-compose -f docker/docker-compose.dev.yml exec web python manage.py createsuperuser

# Load sample data (if you have fixtures)
docker-compose -f docker/docker-compose.dev.yml exec web python manage.py loaddata sample_data.json
```

### Database Backup and Restore
```bash
# Backup database
docker-compose -f docker/docker-compose.dev.yml exec db mysqldump -u saas_user -p saas_platform > backup.sql

# Restore database
docker-compose -f docker/docker-compose.dev.yml exec -T db mysql -u saas_user -p saas_platform < backup.sql
```

### Accessing MySQL Directly
```bash
# Connect to MySQL
docker-compose -f docker/docker-compose.dev.yml exec db mysql -u saas_user -p saas_platform

# Or use root user
docker-compose -f docker/docker-compose.dev.yml exec db mysql -u root -p
```

## 🔧 Development Workflow

### Making Code Changes
With development setup, your code changes are automatically reflected:

1. Edit files in `backend/` or `frontend/` directories
2. Django development server automatically reloads
3. Refresh your browser to see changes

### Installing New Python Packages
```bash
# Add package to requirements.txt
echo "new-package==1.0.0" >> requirements.txt

# Rebuild containers
docker-compose -f docker/docker-compose.dev.yml up --build
```

### Running Tests
```bash
# Run Django tests
docker-compose -f docker/docker-compose.dev.yml exec web python manage.py test

# Run specific test app
docker-compose -f docker/docker-compose.dev.yml exec web python manage.py test apps.authentication
```

## 🔍 Monitoring and Debugging

### Health Checks
```bash
# Check service status
docker-compose -f docker/docker-compose.dev.yml ps

# View container resource usage
docker stats

# Check container health
docker-compose -f docker/docker-compose.dev.yml exec web curl http://localhost:8000/admin/login/
```

### Common Debugging Commands
```bash
# View Django logs
docker-compose -f docker/docker-compose.dev.yml logs web

# Check database connection
docker-compose -f docker/docker-compose.dev.yml exec web python manage.py dbshell

# Check Redis connection
docker-compose -f docker/docker-compose.dev.yml exec redis redis-cli ping
```

## 🌐 Production Deployment

### Environment Configuration
Create `docker/.env` file:
```bash
# Django settings
DEBUG=False
SECRET_KEY=your-very-secure-secret-key
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Database settings
DB_NAME=saas_platform_prod
DB_USER=saas_prod_user
DB_PASSWORD=very-secure-database-password

# Email settings
EMAIL_HOST_USER=noreply@yourdomain.com
EMAIL_HOST_PASSWORD=your-email-password

# Stripe settings
STRIPE_PUBLISHABLE_KEY=pk_live_your_live_key
STRIPE_SECRET_KEY=sk_live_your_live_secret

# SSL settings
SSL_CERT_PATH=/etc/nginx/ssl/cert.pem
SSL_KEY_PATH=/etc/nginx/ssl/key.pem
```

### SSL Certificate Setup
```bash
# Create SSL directory
mkdir -p docker/ssl

# Copy your SSL certificates
cp your-cert.pem docker/ssl/cert.pem
cp your-key.pem docker/ssl/key.pem
```

### Production Deployment
```bash
# Pull latest code
git pull origin main

# Start production services
docker-compose -f docker/docker-compose.yml up --build -d

# Run migrations
docker-compose -f docker/docker-compose.yml exec web python manage.py migrate

# Collect static files
docker-compose -f docker/docker-compose.yml exec web python manage.py collectstatic --noinput

# Create superuser (if needed)
docker-compose -f docker/docker-compose.yml exec web python manage.py createsuperuser
```

## 📊 Scaling and Performance

### Scaling Services
```bash
# Scale web service to 3 instances
docker-compose -f docker/docker-compose.yml up --scale web=3 -d

# Scale celery workers
docker-compose -f docker/docker-compose.yml up --scale celery=2 -d
```

### Resource Limits
Add to docker-compose.yml:
```yaml
services:
  web:
    deploy:
      resources:
        limits:
          cpus: '0.50'
          memory: 512M
        reservations:
          cpus: '0.25'
          memory: 256M
```

## 🚨 Troubleshooting

### Common Issues and Solutions

**Issue: Port already in use**
```bash
# Check what's using the port
lsof -i :8000

# Stop conflicting services
docker-compose down

# Use different ports in docker-compose.yml
ports:
  - "8001:8000"
```

**Issue: Database connection failed**
```bash
# Check database service status
docker-compose ps db

# Check database logs
docker-compose logs db

# Restart database service
docker-compose restart db
```

**Issue: Permission denied errors**
```bash
# Fix file permissions
sudo chown -R $USER:$USER .

# Or run with sudo (not recommended for development)
sudo docker-compose up
```

**Issue: Container builds are slow**
```bash
# Clean up Docker system
docker system prune -a

# Use Docker BuildKit for faster builds
export DOCKER_BUILDKIT=1
docker-compose build
```

**Issue: Out of disk space**
```bash
# Clean up unused Docker resources
docker system df  # Check usage
docker system prune -a --volumes  # Clean everything
```

### Reset Everything
If you need to start fresh:
```bash
# Stop all services
docker-compose -f docker/docker-compose.dev.yml down -v

# Remove all containers and images
docker system prune -a

# Rebuild everything
docker-compose -f docker/docker-compose.dev.yml up --build
```

## 🔄 Backup and Restore

### Complete System Backup
```bash
# Backup database
docker-compose exec db mysqldump -u saas_user -p saas_platform > db_backup.sql

# Backup media files
docker cp $(docker-compose ps -q web):/app/backend/media ./media_backup

# Backup environment configuration
cp docker/.env env_backup
```

### System Restore
```bash
# Restore database
docker-compose exec -T db mysql -u saas_user -p saas_platform < db_backup.sql

# Restore media files
docker cp ./media_backup/. $(docker-compose ps -q web):/app/backend/media

# Restore environment
cp env_backup docker/.env
```

## 📈 Performance Optimization

### Docker Performance Tips
1. **Use .dockerignore** to exclude unnecessary files
2. **Multi-stage builds** for smaller images
3. **Cache layers** by ordering Dockerfile commands properly
4. **Use specific image tags** instead of "latest"
5. **Limit container resources** to prevent resource conflicts

### Monitoring
```bash
# Monitor resource usage
docker stats

# Monitor logs
docker-compose logs -f --tail=100

# Check service health
docker-compose exec web curl -f http://localhost:8000/health/
```

This Docker setup provides a professional, scalable environment for your SaaS platform that can run anywhere! 🚀