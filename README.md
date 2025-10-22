# DevDesk - Developer Issue Tracker

A public, no-login web application for developers to post issues and get community help. Built with Django 5 and Bootstrap 5.

## Features

- Create posts with categories (Bug, CSS, Backend, Frontend, Database, Deployment)
- Public comments with image/GIF support
- Email notifications when comments are added
- Filter by category and status (Open/Solved)
- Responsive Bootstrap 5 UI

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create sample data (optional)
python create_sample_data.py

# Start server
python manage.py runserver
```

Visit http://localhost:8000/

## Admin Access

```bash
python manage.py createsuperuser
```

Then visit http://localhost:8000/admin/

## Tech Stack

- Django 5.2.7
- Python 3.10+
- Bootstrap 5.3.0
- SQLite
- Pillow (image handling)
