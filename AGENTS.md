# Genius CRM - Agent Instructions

## Project Overview
**Genius CRM** - A Django-based CRM platform for Cool Girl Rehab™ personal development brand.

**Stack:** Django, Python, SQLite
**Location:** `/Users/patriciaaraujo/Desktop/Genius CRM /genius`

---

## Critical Conventions

### 1. Lead Tagging System (MANDATORY)
All opt-in forms MUST automatically tag leads with these tags:

1. **Template tag** - e.g., `opt-in-1`, `opt-in-2`
2. **Funnel tag** - auto-generated from funnel name (e.g., `summer_sale_funnel`)
3. **Source tag** - from UTM parameters or default `organic`
4. **Date tag** - `month-year` format (e.g., `march-2026`)
5. **Lead type tag** - e.g., `lead-magnet`, `webinar`, `free-trial`
6. **UTM tags** - `campaign-{name}`, `source-{name}` (if UTM params present)

**UTM URL format for Meta/Facebook ads:**
```
/opt-in/?utm_source=facebook&utm_medium=cpc&utm_campaign=your_campaign_name
```

**Tagging utility:** Use `crm/tagging.py`
```python
from crm.tagging import get_lead_tags, get_utm_data

tags = get_lead_tags(
    request=request,
    template_name='opt-in-1',
    slug='my-funnel',
    lead_type='lead-magnet'
)
```

### 2. URL Routing Order
**CRITICAL:** Always put specific routes BEFORE dynamic routes.
```python
# CORRECT order:
path('opt-in/', views.optin_page, name='optin_page'),
path('opt-in/thank-you/', views.optin_thankyou, name='optin_thankyou'),  # Before slug!
path('opt-in/<slug:slug>/', views.optin_page, name='optin_page_slug'),

# WRONG order (will break):
path('opt-in/<slug:slug>/', ...)  # Catches thank-you!
path('opt-in/thank-you/', ...)     # Never reached
```

### 3. Database Migrations
After modifying models, always run:
```bash
source .venv/bin/activate
python manage.py makemigrations
python manage.py migrate
```

### 4. Server Management
```bash
# Activate venv first
source .venv/bin/activate

# Start server
python manage.py runserver 8000

# Restart server (after code changes)
pkill -f "manage.py runserver" && python manage.py runserver 8000
```

---

## Models

### Contact Model
Key fields for lead tracking:
- `email` (unique)
- `source` - where lead came from
- `utm_source`, `utm_medium`, `utm_campaign`, `utm_content`, `utm_term`
- `tags` - JSON array of tags
- `pipeline_stage` - CRM pipeline status

**Adding tags to contacts:**
```python
contact.tags.append('new-tag')
contact.save()
# Or use built-in method:
contact.add_tag('new-tag')
```

### Funnel Model
- `name` - Display name
- `slug` - URL-safe identifier
- `tag` - Auto-generated from name (updates when name changes)

---

## Templates Location
- **Opt-in templates:** `/genius/funnels/templates/`
- **General templates:** `/genius/templates/`

---

## Email Validation
Located in `crm/validators.py`:
- Blocks disposable emails (mailinator, tempmail, etc.)
- Corrects typos (gmial → gmail)
- Validates format

**DO NOT add API-based verification** unless explicitly requested (costs money, adds delay).

---

## Testing

### Test opt-in form:
```bash
cd "/Users/patriciaaraujo/Desktop/Genius CRM /genius"
source .venv/bin/activate
python manage.py shell -c "
from crm.views import optin_page
from django.test import RequestFactory
factory = RequestFactory()
request = factory.post('/opt-in/?utm_source=test', {
    'first_name': 'Test',
    'last_name': 'User',
    'email': 'test@gmail.com',
    'phone': '12345678',
    'phone_code': '+61'
})
response = optin_page(request)
print('Redirect:', response.url)
"
```

### Check contacts:
```bash
python manage.py shell -c "
from crm.models import Contact
contacts = Contact.objects.order_by('-created_at')[:5]
for c in contacts:
    print(f'{c.first_name}: {c.tags}')
"
```

---

## Git Workflow

1. Make changes
2. Test thoroughly
3. Commit with clear message:
   ```bash
   git add -A
   git commit -m "Description of changes"
   git push origin main
   ```

---

## Pre-Commit Hooks

This project uses pre-commit hooks for code quality and consistency. All hooks are defined in `.pre-commit-config.yaml`.

### Installed Hooks

| Hook | Description | Auto-Fix |
|------|-------------|----------|
| **Django System Checks** | Runs `python manage.py check` | No |
| **Django Tests** | Runs `python manage.py test` | No |
| **Django Migrations Check** | Ensures no unapplied migrations | No |
| **Safety Vulnerability Check** | Scans dependencies for CVEs | No |
| **Trailing Whitespace** | Removes trailing whitespace | Yes |
| **End of File Fixer** | Ensures newline at EOF | Yes |
| **Check YAML** | Validates YAML syntax | No |
| **Check Large Files** | Prevents large file commits | No |
| **Ruff Linter** | Fast Python linter | Yes |
| **Ruff Formatter** | Code formatting | Yes |
| **Black** | PEP-8 code formatting | Yes |
| **isort** | Import sorting | Yes |
| **mypy** | Static type checking | No |
| **Bandit** | Security linting | No |

### Running Pre-Commit

```bash
# Run on all files
pre-commit run --all-files

# Run on staged files only (default on commit)
pre-commit run

# Update hook versions
pre-commit autoupdate
```

### Skipping Hooks

To bypass pre-commit hooks when committing:
```bash
git commit --no-verify -m "Your message"
```

### Virtual Environment

The project uses `uv` for package management. Activate the venv:
```bash
source .venv/bin/activate
```

### Dependencies Location
- **Virtual Environment:** `.venv/`
- **Python Packages:** Installed via `uv pip install`

---

## User Preferences

- **Build incrementally** with approval checkpoints
- **Keep existing styling** - burgundy (#8A0329), lime (#EAFF9D), cream (#F5F0E8)
- **No emojis** in code or commits
- **Concise responses** - answer directly without preamble

---

## Brand Colors
- Burgundy: #8A0329
- Charcoal: #2D2D2D
- Lime: #EAFF9D
- Cream: #F5F0E8

---

**Last Updated:** March 25, 2026

---

## Configuration Files

### pyproject.toml
Contains tool configurations for:
- `black` - Code formatting (line-length: 79, strict PEP-8)
- `isort` - Import sorting (profile: black)
- `ruff` - Linting rules
- `mypy` - Type checking settings
- `bandit` - Security scanning settings

### .pre-commit-config.yaml
Pre-commit hook definitions. See "Pre-Commit Hooks" section above.

### .gitignore
Excludes: `__pycache__`, `.venv`, `db.sqlite3`, IDE files, OS files
