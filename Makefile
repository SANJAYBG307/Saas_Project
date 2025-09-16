.PHONY: help install install-dev migrate test lint format clean run

# Default target
help:
	@echo "Available commands:"
	@echo "  install      Install production dependencies"
	@echo "  install-dev  Install development dependencies"
	@echo "  migrate      Run database migrations"
	@echo "  test         Run tests"
	@echo "  lint         Run linting (flake8, mypy)"
	@echo "  format       Format code (black, isort)"
	@echo "  clean        Clean cache and build files"
	@echo "  run          Run development server"
	@echo "  shell        Open Django shell"
	@echo "  check        Run Django system checks"

# Installation
install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements-dev.txt
	pre-commit install

# Database
migrate:
	cd backend && python manage.py makemigrations
	cd backend && python manage.py migrate

# Testing
test:
	pytest

test-cov:
	pytest --cov=backend --cov-report=html

# Code quality
lint:
	flake8 backend/
	mypy backend/

format:
	black backend/
	isort backend/

# Cleaning
clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	rm -rf .pytest_cache/
	rm -rf htmlcov/
	rm -rf .coverage

# Development
run:
	cd backend && python manage.py runserver

shell:
	cd backend && python manage.py shell

check:
	cd backend && python manage.py check

# Database management
createsuperuser:
	cd backend && python manage.py createsuperuser

collectstatic:
	cd backend && python manage.py collectstatic --noinput

# Reset database (development only)
reset-db:
	rm -f backend/db.sqlite3
	cd backend && python manage.py migrate