# CloudFlow Setup Guide - Step by Step

## 🎯 What You'll Learn

By following this guide, you'll:
- Install all necessary software
- Set up the database
- Configure the application
- Run your first SaaS platform
- Test all features

## 📋 Prerequisites (Software to Install First)

### 1. Python 3.9 or Higher

**Windows:**
1. Go to https://python.org/downloads/
2. Download Python 3.9+ (latest version recommended)
3. **IMPORTANT**: Check "Add Python to PATH" during installation
4. Test installation:
```cmd
python --version
# Should show: Python 3.9.x or higher
```

**Mac:**
```bash
# Using Homebrew (recommended)
brew install python

# Or download from python.org
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
```

### 2. MySQL Database Server

**Windows:**
1. Download MySQL Installer from https://dev.mysql.com/downloads/installer/
2. Choose "Developer Default" setup
3. Set root password (remember this!)
4. Test installation:
```cmd
mysql -u root -p
# Enter your password when prompted
```

**Mac:**
```bash
# Using Homebrew
brew install mysql
brew services start mysql

# Secure installation
mysql_secure_installation
```

**Linux:**
```bash
sudo apt install mysql-server
sudo systemctl start mysql
sudo mysql_secure_installation
```

### 3. Git (Version Control)

**Windows:**
- Download from https://git-scm.com/download/win
- Use default settings during installation

**Mac:**
```bash
# Git comes with Xcode Command Line Tools
xcode-select --install
# Or use Homebrew: brew install git
```

**Linux:**
```bash
sudo apt install git
```

## 🚀 Installation Steps

### Step 1: Download the Project

```bash
# If you have the project files already, skip to Step 2
# Otherwise, if it's in a git repository:
git clone <your-repository-url>
cd ProjectC
```

### Step 2: Create Virtual Environment (Recommended)

A virtual environment keeps this project's packages separate from your system Python.

```bash
# Create virtual environment
python -m venv saas_env

# Activate it:
# Windows:
saas_env\Scripts\activate

# Mac/Linux:
source saas_env/bin/activate

# You should see (saas_env) at the start of your command line
```

### Step 3: Install Python Dependencies

```bash
# Install all required packages
pip install -r requirements.txt

# If you get errors, try:
pip install --upgrade pip
pip install -r requirements.txt
```

**Common Error Solutions:**
- `mysqlclient error`: Install Visual Studio Build Tools (Windows) or `brew install mysql` (Mac)
- `Permission denied`: Use `pip install --user -r requirements.txt`

### Step 4: Database Setup

#### 4.1 Create Database
```bash
# Login to MySQL
mysql -u root -p
# Enter your MySQL password

# Create the database
CREATE DATABASE saas_platform CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

# Create a user for the project (recommended)
CREATE USER 'saas_user'@'localhost' IDENTIFIED BY 'your_password_here';
GRANT ALL PRIVILEGES ON saas_platform.* TO 'saas_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

#### 4.2 Load Database Schema
```bash
# Load the initial database structure
mysql -u root -p saas_platform < database/schema.sql

# Or if using the saas_user:
mysql -u saas_user -p saas_platform < database/schema.sql
```

### Step 5: Configure Environment Variables

```bash
# Copy the example environment file
cp .env.example .env

# Edit the .env file with your settings
```

**Edit `.env` file with your information:**
```bash
# Django Settings
SECRET_KEY=your-very-secret-key-make-it-long-and-random
DEBUG=True

# Database Settings
DB_NAME=saas_platform
DB_USER=saas_user
DB_PASSWORD=your_password_here
DB_HOST=localhost
DB_PORT=3306

# Email Settings (for sending verification emails)
# Use your Gmail account:
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Stripe Settings (for payments) - get these from stripe.com
STRIPE_PUBLISHABLE_KEY=pk_test_your_key_here
STRIPE_SECRET_KEY=sk_test_your_key_here

# Redis (optional, for background tasks)
REDIS_URL=redis://localhost:6379/0
```

**Getting Email App Password (Gmail):**
1. Go to your Google Account settings
2. Enable 2-Step Verification
3. Go to "App passwords"
4. Generate password for "Mail"
5. Use this password in .env file

### Step 6: Django Setup

```bash
# Navigate to backend directory
cd backend

# Run database migrations
python manage.py makemigrations
python manage.py migrate

# Create Django admin user
python manage.py createsuperuser
# Enter username, email, and password when prompted

# Collect static files
python manage.py collectstatic --noinput
```

### Step 7: Start the Server

```bash
# Make sure you're in the backend directory
cd backend

# Start the development server
python manage.py runserver

# You should see output like:
# Watching for file changes with StatReloader
# Performing system checks...
# System check identified no issues (0 silenced).
# Starting development server at http://127.0.0.1:8000/
# Quit the server with CONTROL-C.
```

### Step 8: Test Your Installation

#### 8.1 Open Your Browser

Visit these URLs to test different parts:

1. **Main Website**: http://localhost:8000/
   - Should show beautiful landing page
   - Try clicking "Get Started" and "Login" buttons

2. **Admin Panel**: http://localhost:8000/admin/
   - Login with the superuser account you created
   - Should see Django admin interface

3. **API Test**: http://localhost:8000/api/subscriptions/plans/
   - Should show JSON data for subscription plans

#### 8.2 Test User Registration

1. Click "Get Started" on the landing page
2. Fill out the registration form:
   - Username: testuser
   - Email: your-email@example.com
   - Password: securepassword123
   - Confirm password: securepassword123
   - First/Last name: Your choice
3. Click "Create Account"
4. Should redirect to dashboard (if successful)

#### 8.3 Test Dashboard Access

1. After registering, you should see the dashboard
2. Try creating a new project
3. Add some tasks to the project

## 🛠️ Troubleshooting Common Issues

### Issue: "ModuleNotFoundError: No module named..."

**Solution:**
```bash
# Make sure virtual environment is activated
source saas_env/bin/activate  # Mac/Linux
# or
saas_env\Scripts\activate     # Windows

# Reinstall requirements
pip install -r requirements.txt
```

### Issue: "Access denied for user 'root'@'localhost'"

**Solution:**
```bash
# Reset MySQL root password
sudo mysql
ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'your_new_password';
FLUSH PRIVILEGES;
EXIT;
```

### Issue: "Port 8000 is already in use"

**Solution:**
```bash
# Find what's using port 8000
# Windows:
netstat -ano | findstr :8000

# Mac/Linux:
lsof -i :8000

# Kill the process or use different port:
python manage.py runserver 8001
```

### Issue: "Static files not loading"

**Solution:**
```bash
# Make sure you're serving static files
python manage.py collectstatic

# Check settings.py has correct STATIC_URL
# In development, DEBUG=True should serve static files automatically
```

### Issue: "CSRF token missing or incorrect"

**Solution:**
- Clear browser cache and cookies
- Make sure you're accessing the site through the correct URL (localhost:8000, not 127.0.0.1:8000)

### Issue: Frontend not connecting to backend

**Solution:**
```bash
# Check CORS settings in settings.py
CORS_ALLOWED_ORIGINS = [
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]

# Make sure both frontend and backend use same domain
```

## 🔧 Development Setup (Optional)

### Installing Additional Development Tools

```bash
# Code formatting
pip install black flake8

# Database management tool
pip install django-debug-toolbar

# API testing
pip install httpie
# Test API: http POST localhost:8000/api/auth/login/ username=test password=test
```

### Running in Development Mode

```bash
# Enable debug mode
DEBUG=True in .env file

# Run with auto-reload
python manage.py runserver --reload

# Run on different port
python manage.py runserver 0.0.0.0:8001
```

## 📱 Mobile Testing

To test on your phone:

```bash
# Find your computer's IP address
# Windows: ipconfig
# Mac/Linux: ifconfig

# Start server on all interfaces
python manage.py runserver 0.0.0.0:8000

# Access from phone: http://YOUR_IP_ADDRESS:8000
# Example: http://192.168.1.100:8000
```

## 🚀 Production Setup (Advanced)

### Using Gunicorn (Production Server)

```bash
# Install gunicorn
pip install gunicorn

# Run with gunicorn
cd backend
gunicorn saas_platform.wsgi:application --bind 0.0.0.0:8000
```

### Environment Variables for Production

```bash
# Production .env settings
DEBUG=False
SECRET_KEY=very-long-random-key-for-production
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Use production database
DB_HOST=your-production-db-host
DB_PASSWORD=strong-production-password

# Production email
EMAIL_HOST_USER=noreply@yourdomain.com

# Production Stripe keys
STRIPE_PUBLISHABLE_KEY=pk_live_...
STRIPE_SECRET_KEY=sk_live_...
```

## ✅ Verification Checklist

Before considering setup complete, verify:

- [ ] Python and pip working (`python --version`)
- [ ] MySQL running and accessible (`mysql -u root -p`)
- [ ] Virtual environment activated (see `(saas_env)` in terminal)
- [ ] All pip packages installed without errors
- [ ] Database created and schema loaded
- [ ] .env file configured with your settings
- [ ] Django migrations completed
- [ ] Superuser created
- [ ] Server starts without errors (`python manage.py runserver`)
- [ ] Landing page loads in browser
- [ ] User registration works
- [ ] Dashboard accessible after login
- [ ] Admin panel accessible

## 🆘 Getting Help

If you're still stuck:

1. **Check the error message carefully** - most errors tell you exactly what's wrong
2. **Google the exact error message** - others have likely encountered it
3. **Check Django documentation** - https://docs.djangoproject.com/
4. **Verify your Python/MySQL versions** match requirements
5. **Try creating a fresh virtual environment** if package issues persist

## 🎉 Success!

If you've reached this point with everything working, congratulations! You now have a fully functional SaaS platform running on your computer.

Next steps:
- Explore the code in `docs/code_explanations/`
- Try customizing the frontend design
- Add new features to the dashboard
- Set up payment processing with Stripe

Happy coding! 🚀