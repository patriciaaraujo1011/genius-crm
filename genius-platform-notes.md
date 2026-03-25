# Genius Platform - Project Notes

## Project Overview
**Genius CRM** - Django-based unified platform replacing Kajabi, Go High Level, Skool, and Stan.

**Current Stack:**
- Django 4.x
- SQLite database
- Stripe for payments
- Pre-commit hooks (ruff, black, isort, mypy, bandit, safety)

---

## Project Structure

```
genius/
├── crm/
│   ├── models.py       # Contact, Product, Funnel, Order, etc.
│   ├── views.py        # All view functions
│   ├── admin.py        # Admin configuration
│   ├── stripe_utils.py # Stripe integration
│   └── tests.py        # Unit tests
├── templates/
│   ├── base.html       # Main CRM layout
│   ├── funnels.html    # Funnels page
│   ├── funnel_templates.html
│   └── funnel/templates/
│       └── sales_template_1.html  # CGR funnel template
├── genius_platform/
│   ├── settings.py
│   └── urls.py
└── .venv/             # Virtual environment
```

---

## Key Models

| Model | Purpose |
|-------|---------|
| `Contact` | Leads/customers with tags, UTM tracking |
| `Product` | Digital products/courses for sale |
| `Order` | Purchase records with Stripe IDs |
| `Funnel` | Sales funnel with offer settings |
| `FunnelPage` | Individual pages within funnels |
| `OrderBump` | Additional products on order page |
| `EmailSequence` | Automated email sequences |
| `Broadcast` | Email broadcasts |

---

## Funnel System

### Templates Location
`templates/funnel/templates/`

### Available Templates
1. `sales_template_1.html` - Landing/sales page (done)
2. `order_template_1.html` - Checkout page (TODO)
3. `upsell_template_1.html` - Post-purchase upsell (TODO)
4. `thank_you_template_1.html` - Confirmation page (TODO)

### Funnel URLs
- `/funnel/<slug>/` - Sales page
- `/funnel/<slug>/order/` - Order page
- `/funnel/<slug>/checkout/` - POST checkout
- `/funnel/<slug>/upsell/` - Upsell page
- `/funnel/<slug>/thank-you/` - Thank you page

---

## Testing

**Run tests:**
```bash
cd genius && source .venv/bin/activate && python manage.py test
```

**Pre-commit hooks:**
```bash
cd genius && source .venv/bin/activate && pre-commit run --all-files
```

---

## Development Workflow

1. Make changes
2. Run tests: `python manage.py test`
3. Run pre-commit: `pre-commit run --all-files`
4. Commit and push

---

## Common Issues

### Server not running
```bash
cd genius && source .venv/bin/activate && python manage.py runserver 8080
```

### Import errors after git pull
- Check for merge conflicts: `git status`
- Resolve conflicts manually

---

## Git Commands

```bash
# Commit changes
git add -A && git commit -m "message"

# Push
git push

# Pull and resolve
git pull origin main --ff
```

---

**Last Updated:** March 26, 2026
