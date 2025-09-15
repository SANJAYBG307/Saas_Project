# Requirements and Dependencies Explanation

## What Each Package Does (Simple English)

### Core Framework
- **Django==4.2.7**: Main web framework (like the foundation of a house)
- **djangorestframework==3.14.0**: Helps create APIs (ways for frontend to talk to backend)

### Database Connection
- **mysqlclient==2.2.0**: Connects Python to MySQL database
- **django-environ==0.11.2**: Manages secret settings (like passwords) safely

### User Authentication (Login/Register System)
- **django-allauth==0.57.0**: Handles user registration, login, password reset
- **djangorestframework-simplejwt==5.3.0**: Creates secure login tokens
- **django-cors-headers==4.3.1**: Allows frontend and backend to communicate

### Multi-Tenant Support (Multiple Companies Using Same App)
- **django-tenant-schemas==1.10.0**: Separates data for different companies
- **django-tenants==3.5.0**: Advanced multi-tenant features

### Payment System
- **stripe==7.8.0**: Handles credit card payments
- **django-stripe-payments==1.0.0**: Integrates Stripe with Django

### Admin Interface (For Managing the Platform)
- **django-admin-interface==0.28.6**: Makes admin panel look beautiful
- **django-colorfield==0.10.1**: Adds color picker to admin

### Email System
- **django-sendgrid-v5==1.2.3**: Sends emails (welcome, password reset, etc.)

### Utilities
- **Pillow==10.1.0**: Handles image processing (profile pictures, logos)
- **python-decouple==3.8**: Manages configuration settings
- **celery==5.3.4**: Handles background tasks (like sending emails)
- **redis==5.0.1**: Fast temporary storage for background tasks

### Development Tools (For Testing While Building)
- **django-debug-toolbar==4.2.0**: Shows debugging information
- **django-extensions==3.2.3**: Extra helpful commands

### Production Server (For Live Website)
- **gunicorn==21.2.0**: Web server to run the application
- **whitenoise==6.6.0**: Serves CSS/JS files efficiently

### Testing Tools
- **pytest==7.4.3**: Framework for writing tests
- **pytest-django==4.7.0**: Django-specific testing tools
- **factory-boy==3.3.0**: Creates fake data for testing

### Docker Support (For Running on Any Computer)
- **psycopg2-binary==2.9.9**: Alternative database connector

## Version Information
- **Python Version Required**: 3.9 or higher
- **Django Version**: 4.2.7 (LTS - Long Term Support)
- **All versions are tested and compatible with each other**

## Installation Command
```bash
pip install -r requirements.txt
```