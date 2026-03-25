# Genius - CRM Platform

A Django-based CRM platform for **Cool Girl Rehab™** - Personal Development Brand for High Achieving Women.

## Features

- **Dashboard** - Overview stats (contacts, orders, revenue)
- **Contacts** - Manage leads and customers
- **Products** - Courses, memberships, digital products
- **Orders** - Track purchases
- **Funnels** - Sales funnel pages (landing, order, thank you)
- **Courses** - Module-based course content
- **Broadcast** - One-time email sends
- **Email Sequences** - Automated drip campaigns

## Tech Stack

- Django 4.2
- SQLite (development)
- Vanilla HTML/CSS templates

## Setup

```bash
# Install Django
pip install django

# Run migrations
python manage.py migrate

# Create admin user
python manage.py createsuperuser

# Run server
python manage.py runserver
```

## Login

- URL: http://127.0.0.1:8000/
- Admin: http://127.0.0.1:8000/admin/

## Build Phases (Email Marketing System)

See full build plan in project documentation.

- Phase 1A: Contact System + Email Validation
- Phase 1B: Pipeline System
- Phase 1C: Email Sending (SendGrid/Mailgun)
- Phase 1D: Sequence Automation
- Phase 1E: Analytics Dashboard
