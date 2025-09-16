# Complete VS Code Setup Guide - CloudFlow SaaS Platform

## **STEP 1: Install Required Software**

### **1.1 Install VS Code**
```bash
# Download VS Code from: https://code.visualstudio.com/
# Or if you have Homebrew on Mac:
brew install --cask visual-studio-code

# Or on Windows: Download from website and install
# Or on Linux:
sudo snap install code --classic
```

### **1.2 Install Python**
```bash
# Check if Python is installed
python3 --version

# If not installed:
# Mac: brew install python@3.9
# Windows: Download from python.org
# Linux: sudo apt install python3.9 python3.9-pip
```

### **1.3 Install MySQL**
```bash
# Mac:
brew install mysql
brew services start mysql

# Windows: Download MySQL Installer from mysql.com
# Linux:
sudo apt install mysql-server
sudo systemctl start mysql
```

---

## **STEP 2: Open Project in VS Code**

### **2.1 Open VS Code and Load Project**
```bash
# Method 1: Command line (recommended)
cd /Users/pims/Desktop/ProjectC
code .

# Method 2: VS Code GUI
# 1. Open VS Code
# 2. File → Open Folder
# 3. Navigate to /Users/pims/Desktop/ProjectC
# 4. Click "Open"
```

### **2.2 Install Required VS Code Extensions**
When VS Code opens, install these extensions:

1. **Python** (by Microsoft) - Essential for Python development
2. **Django** (by Baptiste Darthenay) - Django template support
3. **MySQL** (by Jun Han) - Database management
4. **GitLens** (by GitKraken) - Git integration
5. **Prettier** - Code formatting

**How to install:**
- Press `Ctrl+Shift+X` (Windows/Linux) or `Cmd+Shift+X` (Mac)
- Search for each extension
- Click "Install"

---

## **STEP 3: Setup Python Environment**

### **3.1 Create Virtual Environment**
In VS Code Terminal (`Terminal → New Terminal`):

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On Mac/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate

# You should see (venv) in your terminal prompt
```

### **3.2 Select Python Interpreter in VS Code**
1. Press `Ctrl+Shift+P` (Windows/Linux) or `Cmd+Shift+P` (Mac)
2. Type "Python: Select Interpreter"
3. Choose the one that shows `./venv/bin/python` or `./venv/Scripts/python.exe`

### **3.3 Install Dependencies**
```bash
# Install all dependencies
make install-dev

# Or manually:
pip install -r requirements-dev.txt
```

---

## **STEP 4: Setup Database**

### **4.1 Start MySQL Service**
```bash
# Check if MySQL is running
brew services list | grep mysql

# Start MySQL if not running
brew services start mysql

# Or on Linux:
sudo systemctl start mysql
```

### **4.2 Create Database and User**
```bash
# Connect to MySQL
mysql -u root -p
# Enter your MySQL root password when prompted

# In MySQL prompt, run these commands:
CREATE DATABASE saas_platform CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'Saas_User'@'localhost' IDENTIFIED BY 'Saas@123';
GRANT ALL PRIVILEGES ON saas_platform.* TO 'Saas_User'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

### **4.3 Verify Database Connection**
```bash
# Test connection with the new user
mysql -u Saas_User -p saas_platform
# Enter password: Saas@123
# If successful, you'll see MySQL prompt
EXIT;
```

---

## **STEP 5: Start the Application**

### **5.1 Run Database Migrations**
```bash
# In VS Code terminal (make sure venv is activated)
make migrate

# Or manually:
cd backend
python manage.py makemigrations
python manage.py migrate
```

### **5.2 Create Admin User**
```bash
make createsuperuser

# Or manually:
cd backend
python manage.py createsuperuser

# Follow prompts:
# Username: admin
# Email: admin@example.com
# Password: (enter a strong password)
```

### **5.3 Start Development Server**
```bash
# Method 1: Using Makefile (recommended)
make run

# Method 2: Manual
cd backend
python manage.py runserver

# Method 3: VS Code Debug (F5 key)
# Press F5 and select "Django" configuration
```

**You should see output like:**
```
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
Django version 4.2.7, using settings 'saas_platform.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

---

## **STEP 6: Access Your Application**

### **6.1 Open in Browser**
Open these URLs in your web browser:

1. **Main Landing Page**: http://127.0.0.1:8000/
   - Your beautiful frontend with signup/login buttons

2. **Django Admin Panel**: http://127.0.0.1:8000/admin/
   - Login with the superuser credentials you created
   - Manage users, subscriptions, etc.

3. **API Endpoints**: http://127.0.0.1:8000/api/
   - REST API for frontend-backend communication

### **6.2 Test the Application**
1. **Landing Page**: You should see CloudFlow homepage
2. **Registration**: Click "Get Started" to create an account
3. **Login**: Use login button to access dashboard
4. **Admin Panel**: Access backend management

### **6.3 Serve Frontend Properly** (Optional)
```bash
# In a second terminal, serve frontend files
cd frontend
python -m http.server 3000

# Now access: http://localhost:3000
```

---

## **STEP 7: VS Code Development Features**

### **7.1 Debugging**
```bash
# Set breakpoints by clicking left of line numbers
# Press F5 to start debugging
# Choose "Django" configuration
# Server starts in debug mode - you can step through code
```

### **7.2 Running Tests**
```bash
# In terminal:
make test

# Or in VS Code:
# 1. Open Testing panel (Ctrl+Shift+T)
# 2. Click "Configure Python Tests"
# 3. Select "pytest"
# 4. Select "backend" as root directory
# 5. Run tests by clicking play buttons
```

### **7.3 Code Quality Tools**
```bash
# Format code
make format

# Check code quality
make lint

# All in one check
make test && make lint
```

### **7.4 Database Management**
```bash
# Django shell for database queries
make shell
# Or: cd backend && python manage.py shell

# Create new migrations after model changes
cd backend
python manage.py makemigrations

# Apply migrations
python manage.py migrate
```

---

## **🎯 QUICK SUMMARY - Essential Commands**

### **Every Time You Start Development:**
```bash
# 1. Open project
cd /Users/pims/Desktop/ProjectC
code .

# 2. Activate virtual environment
source venv/bin/activate

# 3. Start server
make run

# 4. Open browser to http://127.0.0.1:8000/
```

### **Daily Development Workflow:**
```bash
# Check code quality before committing
make format
make lint
make test

# Run server
make run

# Access admin panel
# http://127.0.0.1:8000/admin/
```

---

## **🚨 Troubleshooting Common Issues**

### **Issue 1: "Module not found" errors**
```bash
# Make sure virtual environment is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements-dev.txt
```

### **Issue 2: Database connection errors**
```bash
# Check MySQL is running
brew services list | grep mysql
brew services start mysql

# Verify database exists
mysql -u Saas_User -p saas_platform
```

### **Issue 3: Port already in use**
```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9

# Or use different port
cd backend
python manage.py runserver 8001
```

### **Issue 4: VS Code not recognizing Python**
1. Press `Cmd+Shift+P`
2. Type "Python: Select Interpreter"
3. Choose `./venv/bin/python`

### **Issue 5: Virtual environment issues**
```bash
# Delete and recreate virtual environment
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements-dev.txt
```

### **Issue 6: MySQL installation issues**
```bash
# Mac - if brew install mysql fails:
brew update
brew doctor
brew install mysql

# Ubuntu - if apt install fails:
sudo apt update
sudo apt install mysql-server mysql-client
```

---

## **🔧 Advanced VS Code Configuration**

### **Useful VS Code Shortcuts:**
- `Cmd+Shift+P` / `Ctrl+Shift+P`: Command palette
- `Cmd+P` / `Ctrl+P`: Quick file open
- `F5`: Start debugging
- `Ctrl+Shift+T`: Open test panel
- `Cmd+J` / `Ctrl+J`: Toggle terminal
- `Cmd+Shift+E` / `Ctrl+Shift+E`: Explorer panel

### **Customizing Settings:**
The project includes `.vscode/settings.json` with optimized settings for:
- Python formatting with Black
- Import sorting with isort
- Code linting with Flake8
- Test discovery with pytest

### **Debug Configuration:**
The project includes `.vscode/launch.json` with configurations for:
- Django development server debugging
- Django test debugging

---

## **📚 Additional Resources**

### **Learning VS Code:**
- VS Code Documentation: https://code.visualstudio.com/docs
- Python in VS Code: https://code.visualstudio.com/docs/python/python-tutorial
- Django in VS Code: https://code.visualstudio.com/docs/python/tutorial-django

### **Django Development:**
- Django Documentation: https://docs.djangoproject.com/
- Django REST Framework: https://www.django-rest-framework.org/

### **Project Structure:**
- See `PROJECT_STRUCTURE.md` for detailed project organization
- See `CONTRIBUTING.md` for development guidelines
- See `README.md` for project overview

---

**🎉 Happy Coding!** You now have a complete professional development environment for your SaaS platform!

---

## **📝 Notes**

- Keep this file updated as you make changes to the setup process
- Share this with team members for consistent development environment
- If you encounter issues not covered here, document the solution for future reference