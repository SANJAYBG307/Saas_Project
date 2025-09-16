# Local Development Setup

This guide will help you run the SaaS Platform locally without Docker in any code editor like VS Code, PyCharm, etc.

## Prerequisites

- Python 3.9 or higher
- pip (Python package installer)
- MySQL Server 8.0+ installed and running
- A code editor (VS Code, PyCharm, Sublime Text, etc.)

## Setup Instructions

### 1. Install Python Dependencies

```bash
# Navigate to the project root
cd /path/to/ProjectC

# Install the required packages
pip install -r requirements.txt
```

### 2. Database Setup

**Create MySQL Database and User:**

```sql
-- Connect to MySQL as root
mysql -u root -p

-- Create database
CREATE DATABASE saas_platform CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Create user and grant privileges
CREATE USER 'Saas_User'@'localhost' IDENTIFIED BY 'Saas@123';
GRANT ALL PRIVILEGES ON saas_platform.* TO 'Saas_User'@'localhost';
FLUSH PRIVILEGES;

-- Exit MySQL
EXIT;
```

**Environment Configuration:**

The database configuration is already set in `.env` file with your MySQL credentials:
- Database: `saas_platform`
- User: `Saas_User`
- Password: `Saas@123`
- Host: `localhost`
- Port: `3306`

### 3. Django Database Setup

```bash
# Navigate to the backend directory
cd backend

# Create and apply database migrations
python manage.py makemigrations
python manage.py migrate

# Create a superuser for admin access
python manage.py createsuperuser
```

### 4. Run the Django Development Server

```bash
# From the backend directory
python manage.py runserver

# The server will start at http://127.0.0.1:8000/
```

### 5. Access the Application

- **Frontend**: Open `frontend/index.html` directly in a browser, or serve it with a simple HTTP server:
  ```bash
  # From the frontend directory
  python -m http.server 3000
  # Then visit http://localhost:3000
  ```

- **Django Admin**: http://127.0.0.1:8000/admin/
- **API Endpoints**: http://127.0.0.1:8000/api/

## Development Workflow

### Code Editor Setup

1. **VS Code**:
   - Open the project folder in VS Code
   - Install Python extension
   - Set Python interpreter to your virtual environment (if using one)

2. **PyCharm**:
   - Open the project folder
   - Configure Python interpreter
   - Set Django settings module: `saas_platform.settings`

### Making Changes

1. **Backend Changes**:
   - Edit Django files in the `backend/` directory
   - The development server will auto-reload on changes

2. **Frontend Changes**:
   - Edit HTML, CSS, or JavaScript files in `frontend/` directory
   - Refresh browser to see changes

### Database Changes

When you modify models:
```bash
cd backend
python manage.py makemigrations
python manage.py migrate
```

## Optional Features

### Multi-tenancy
The project uses django-tenants. For local development, you may want to:
1. Create a tenant in the admin panel
2. Set up a domain for testing

### Celery (Background Tasks)
Celery is commented out for local development. To enable:
1. Install and run Redis locally
2. Uncomment Celery settings in `settings.py`
3. Run: `celery -A saas_platform worker -l info`

### Email Testing
For email testing, you can use Django's console backend by adding this to `settings.py`:
```python
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

## Troubleshooting

### Common Issues

1. **Module not found**: Make sure you're in the correct directory and have installed all requirements
2. **MySQL connection errors**:
   - Ensure MySQL server is running: `sudo service mysql start` (Linux) or check MySQL in System Preferences (Mac)
   - Verify database and user exist: `mysql -u Saas_User -p saas_platform`
   - Check credentials in `.env` file
3. **mysqlclient installation errors**:
   - On Mac: `brew install mysql pkg-config`
   - On Ubuntu: `sudo apt-get install python3-dev default-libmysqlclient-dev build-essential`
4. **Port already in use**: Use a different port: `python manage.py runserver 8001`

### Getting Help

Check the `docs/` directory for additional documentation about specific features.