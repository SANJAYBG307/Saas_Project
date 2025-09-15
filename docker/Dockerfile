# Use official Python runtime as base image
FROM python:3.9-slim as base

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE=saas_platform.settings

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client \
        default-mysql-client \
        gcc \
        default-libmysqlclient-dev \
        pkg-config \
        curl \
    && rm -rf /var/lib/apt/lists/*

# Copy Python requirements and install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Development stage
FROM base as development
# Copy project
COPY . /app/

# Copy frontend files to static directory
RUN mkdir -p /app/backend/static/
COPY frontend/ /app/backend/static/

# Change to backend directory for Django commands
WORKDIR /app/backend

# Expose port
EXPOSE 8000

# Command to run the application in development
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

# Production stage
FROM base as production
# Copy project
COPY . /app/

# Copy frontend files to static directory
RUN mkdir -p /app/backend/static/
COPY frontend/ /app/backend/static/

# Change to backend directory for Django commands
WORKDIR /app/backend

# Collect static files
RUN python manage.py collectstatic --noinput

# Create non-root user
RUN adduser --disabled-password --gecos '' appuser
RUN chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/admin/login/ || exit 1

# Command to run the application in production
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "saas_platform.wsgi:application"]