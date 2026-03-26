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

---

## Testing Rule (MANDATORY)

Before saying any work is "done" or "ready":

1. **Always test the actual functionality** - not just verify code exists
2. **Test, re-test, and test again** - at least 3 verification steps
3. **Check the actual browser output** - verify curl/HTML contains expected elements
4. **Never assume it works** - always verify with actual tests
5. **Report exact test results** - not just "it should work"

Example verification process:
```bash
# 1. Check endpoint returns 200
curl -s -o /dev/null -w "%{http_code}" "http://localhost:8000/url/"
# 2. Verify content contains expected elements
curl -s "http://localhost:8000/url/" | grep "expected-element"
# 3. Check JavaScript functions exist
curl -s "http://localhost:8000/url/" | grep "function-name"
```

**Never tell the user "it should work" without verifying it actually does.**

---

## Comprehensive Testing Checklist (MANDATORY)

For any feature, always verify ALL of these BEFORE saying done:

### 1. Test Every Single Page/Template
- Check ALL pages in the feature work (not just one)
- Example: If feature has 4 templates, test ALL 4

### 2. Test Every Interactive Element
- Every button
- Every link (a href)
- Every form input
- Every onclick handler
- Every CTA button
- Every navigation element

### 3. Use This Exact Testing Process
```bash
# 1. Check all pages return 200
curl -s -o /dev/null -w "%{http_code}" "http://localhost:8000/page1/"
curl -s -o /dev/null -w "%{http_code}" "http://localhost:8000/page2/"

# 2. Find ALL buttons/links
curl -s "http://localhost:8000/page/" | grep -oE "(href=|onclick=|<button|<a )"

# 3. Check CSS disables all elements
curl -s "http://localhost:8000/page/" | grep "pointer-events"

# 4. Open in browser and manually click EVERY button
```

### 4. Interactive Elements to Check
- `<button>` tags
- `<a href="...">` links
- `onclick="..."` handlers
- `input[type="submit"]`
- Classes: cta-btn, form-submit, access-cta, btn, button

### 5. When Done, Report This
- How many pages tested
- How many buttons/links found
- How many tested manually in browser
- Exact issues found (if any)

---

## Template Preview Modal (MANDATORY)

When creating template preview functionality in the CRM, use this proven approach:

### The Working Solution: iframe with srcdoc

```html
<style>
#previewModal {
  display: none;
  position: fixed;
  top: 5%;
  left: 5%;
  width: 90%;
  height: 90%;
  background: #0B0A09;
  border-radius: 10px;
  box-shadow: 0 10px 50px rgba(0,0,0,0.8);
  z-index: 999999;
}
#previewModal.show {
  display: flex;
  flex-direction: column;
}
#previewHeader {
  height: 45px;
  background: #1a1a1a;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 15px;
  flex-shrink: 0;
}
#previewClose {
  background: #8A0329;
  border: none;
  color: white;
  width: 30px;
  height: 30px;
  border-radius: 50%;
  cursor: pointer;
}
#previewFrame {
  flex: 1;
  width: 100%;
  border: none;
  border-radius: 0 0 10px 10px;
  background: white;
}
</style>

<!-- Preview Buttons -->
<button type="button" class="preview-btn" data-url="/preview/sales/">Preview</button>

<!-- Modal -->
<div id="previewModal">
  <div id="previewHeader">
    <span>Template Preview</span>
    <button type="button" id="previewClose">X</button>
  </div>
  <iframe id="previewFrame"></iframe>
</div>

<script>
document.addEventListener('DOMContentLoaded', function() {
  var modal = document.getElementById('previewModal');
  var frame = document.getElementById('previewFrame');
  var closeBtn = document.getElementById('previewClose');
  var buttons = document.querySelectorAll('.preview-btn');

  buttons.forEach(function(btn) {
    btn.addEventListener('click', function() {
      var url = btn.getAttribute('data-url');
      fetch(url)
        .then(function(response) { return response.text(); })
        .then(function(html) {
          // Add preview mode styles to disable buttons and add banner
          var previewStyles = '<style>' +
            '#previewModeBanner { position: fixed; top: 10px; right: 10px; background: #8A0329; color: white; padding: 8px 16px; border-radius: 4px; font-size: 12px; font-weight: bold; z-index: 999999; } ' +
            '#previewModeBanner::before { content: "👁️ PREVIEW MODE - "; } ' +
            '/* Disable all clickable elements */ ' +
            '#page-sales a[href], #page-sales button, #page-sales input[type="submit"], ' +
            '#page-order a[href], #page-order button, #page-order input[type="submit"], ' +
            '#page-upsell a[href], #page-upsell button, #page-upsell input[type="submit"], ' +
            '#page-thankyou a[href], #page-thankyou button, #page-thankyou input[type="submit"], ' +
            '.cta-btn, .cta-yes, .cta-decline, .form-submit, .access-cta, ' +
            '[onclick] { pointer-events: none !important; opacity: 0.4 !important; cursor: not-allowed !important; } ' +
            '/* Keep dev-bar working */ ' +
            '.dev-bar, .dev-bar *, .dev-btn { pointer-events: auto !important; opacity: 1 !important; cursor: pointer !important; } ' +
            '</style>';

          // Insert banner
          html = html.replace('<body>', '<body><div id="previewModeBanner"></div>');

          // Add script to disable onclick handlers after load
          var disableScript = '<script>document.querySelectorAll("[onclick]").forEach(function(el){if(!el.classList.contains("dev-btn")){el.removeAttribute("onclick");}});document.querySelectorAll("a[href]").forEach(function(el){if(!el.classList.contains("dev-btn")){el.setAttribute("data-href",el.getAttribute("href"));el.removeAttribute("href");}});<\/script>';

          frame.srcdoc = previewStyles + html + disableScript;
          modal.classList.add('show');
        });
    });
  });

  closeBtn.addEventListener('click', function() {
    modal.classList.remove('show');
    frame.srcdoc = '';
  });

  document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
      modal.classList.remove('show');
      frame.srcdoc = '';
    }
  });
});
</script>
```

### Why This Works
- **srcdoc** completely isolates template CSS from CRM styles
- **iframe** provides proper scrolling context
- **fetch + srcdoc** loads HTML dynamically without CORS issues
- **DOMContentLoaded** ensures JavaScript runs after DOM is ready
- **Disables ALL buttons/links** - CSS + JavaScript removal of href/onclick
- **Preview banner** - Shows user they are in preview mode
- **Keeps dev-bar working** - Mobile/desktop toggle still functions
4. Add Escape key handler for accessibility
5. Test on multiple templates before finalizing

### Preview Routes Required
For each template, create a preview URL endpoint that renders just the template HTML:
```python
path("preview/sales/", views.preview_sales, name="preview_sales"),
path("preview/order/", views.preview_order, name="preview_order"),
# etc.
```
