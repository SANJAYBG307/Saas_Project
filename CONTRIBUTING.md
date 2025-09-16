# Contributing to CloudFlow

## Development Setup

### Prerequisites
- Python 3.9+
- MySQL 8.0+
- Git

### Setup Development Environment

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ProjectC
   ```

2. **Install development dependencies**
   ```bash
   make install-dev
   ```

3. **Setup pre-commit hooks**
   ```bash
   pre-commit install
   ```

4. **Configure database**
   ```bash
   # Create database and user (see README.md)
   make migrate
   ```

## Development Workflow

### Code Quality Standards

This project follows strict code quality standards:

- **Black** for code formatting
- **Flake8** for linting
- **isort** for import sorting
- **mypy** for type checking
- **pytest** for testing

### Before Committing

Always run these commands before committing:

```bash
make format      # Format code
make lint        # Check code quality
make test        # Run tests
```

### Running Tests

```bash
# Run all tests
make test

# Run with coverage
make test-cov

# Run specific test file
pytest backend/apps/authentication/tests.py

# Run specific test
pytest backend/apps/authentication/tests.py::AuthenticationViewTests::test_user_registration
```

### Code Style Guidelines

1. **Python Code**:
   - Follow PEP 8
   - Use type hints
   - Write docstrings for functions and classes
   - Keep functions under 50 lines

2. **Django**:
   - Use class-based views where appropriate
   - Keep models simple and focused
   - Use Django's built-in features

3. **Testing**:
   - Write tests for all new features
   - Maintain >80% code coverage
   - Use meaningful test names

### Project Structure

- `backend/apps/` - Django applications
- `frontend/` - Static frontend files
- `docs/` - Documentation
- `tests/` - Test files (inside each app)

### Making Changes

1. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Write code
   - Add tests
   - Update documentation

3. **Test your changes**
   ```bash
   make test
   make lint
   ```

4. **Commit your changes**
   ```bash
   git add .
   git commit -m "feat: add your feature description"
   ```

5. **Push and create PR**
   ```bash
   git push origin feature/your-feature-name
   ```

### Commit Message Format

Use conventional commits:

- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `test:` - Adding tests
- `refactor:` - Code refactoring

## Adding New Features

### Adding a New Django App

1. Create the app:
   ```bash
   cd backend
   python manage.py startapp your_app_name apps/
   ```

2. Add to `INSTALLED_APPS` in `settings.py`

3. Create the required files:
   - `apps.py` - App configuration
   - `tests.py` - Test cases
   - `urls.py` - URL routing

### Adding API Endpoints

1. Create serializers in `serializers.py`
2. Create views in `views.py`
3. Add URLs in `urls.py`
4. Write tests in `tests.py`

### Adding Frontend Features

1. Update HTML templates
2. Add CSS in `frontend/css/`
3. Add JavaScript in `frontend/js/`
4. Test responsive design

## Testing Guidelines

### Writing Good Tests

1. **Test Names**: Use descriptive names
   ```python
   def test_user_can_register_with_valid_data(self):
   ```

2. **Test Structure**: Follow AAA pattern
   ```python
   def test_example(self):
       # Arrange
       user_data = {...}

       # Act
       response = self.client.post(url, user_data)

       # Assert
       self.assertEqual(response.status_code, 201)
   ```

3. **Use Fixtures**: Create reusable test data
   ```python
   def setUp(self):
       self.user = User.objects.create_user(...)
   ```

### Test Categories

- **Unit Tests**: Test individual functions/methods
- **Integration Tests**: Test component interactions
- **API Tests**: Test HTTP endpoints

## Documentation

### Code Documentation

- Add docstrings to all functions and classes
- Use type hints for function parameters and returns
- Comment complex logic

### API Documentation

- Document all API endpoints
- Include request/response examples
- Specify required parameters

## Getting Help

- Check existing documentation in `docs/`
- Look at similar code in the project
- Ask questions in issues or discussions

## Code Review Process

1. All changes must be reviewed
2. Tests must pass
3. Code coverage must not decrease
4. Follow coding standards
5. Update documentation if needed

Thank you for contributing to CloudFlow! 🚀