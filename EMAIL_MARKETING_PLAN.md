# Genius CRM - Email Marketing Build Plan

## Phase 1: Foundation - Email Sending

| # | Feature | What It Is | Effort |
|---|---------|------------|--------|
| 1 | **Email Settings** | Configure SMTP or console backend | Small |
| 2 | **Send Functions** | Create email_utils.py with send functions | Small |
| 3 | **Connect Send Button** | Link Broadcast UI to email function | Small |

## Phase 2: Broadcast Features

| # | Feature | What It Is | Effort |
|---|---------|------------|--------|
| 4 | **Segment Filtering** | Filter contacts by tag (buyers, leads, etc.) | Medium |
| 5 | **Save as Draft** | Save broadcast without sending | Small |
| 6 | **Schedule for Later** | Set send date/time | Medium |
| 7 | **Preview Email** | See email before sending | Small |

## Phase 3: Email Branding (Critical)

| # | Feature | What It Is | Effort |
|---|---------|------------|--------|
| 8 | **Base Email Template** | Master template with header/footer | Medium |
| 9 | **Brand Colors in CSS** | Your pink (#e93d3d), orange, cream in email | Small |
| 10 | **Fonts in Email** | Inter font loaded in email HTML | Small |
| 11 | **Logo Variable** | {{ logo_url }} template variable | Small |
| 12 | **Unsubscribe Link** | Legal requirement (GDPR) | Small |
| 13 | **Social Links** | Instagram, etc. in footer | Small |
| 14 | **Company Address** | Legal requirement in footer | Small |
| 15 | **CSS Inlining** | Convert CSS to inline styles for email clients | Medium |
| 16 | **Email Signature** | Your personal sign-off template | Small |

## Phase 4: Sequences Features

| # | Feature | What It Is | Effort |
|---|---------|------------|--------|
| 17 | **Trigger Logic** | Detect when to send (opt-in, purchase) | Medium |
| 18 | **Delay Processing** | Wait X hours/days between emails | Medium |
| 19 | **Condition Logic** | If opened → send different email | Medium |
| 20 | **Exit Conditions** | Stop when purchased, unsubscribed | Small |

## Phase 5: Template Library

| # | Feature | What It Is | Effort |
|---|---------|------------|--------|
| 21 | **Welcome Template** | Branded welcome email | Medium |
| 22 | **Nurture Template** | Branded nurture sequence email | Medium |
| 23 | **Promo Template** | Branded promotional email | Medium |
| 24 | **Receipt Template** | Branded purchase receipt | Medium |

## Phase 6: Tracking & Analytics

| # | Feature | What It Is | Effort |
|---|---------|------------|--------|
| 25 | **Contact Email Log** | Track who got which email | Medium |
| 26 | **Open Tracking** | Track when emails are opened | Medium |
| 27 | **Click Tracking** | Track when links are clicked | Medium |
| 28 | **Broadcast Analytics** | Open rate, click rate per broadcast | Medium |
| 29 | **Revenue Attribution** | Track sales from emails | Medium |

## Phase 7: Advanced Features

| # | Feature | What It Is | Effort |
|---|---------|------------|--------|
| 30 | **A/B Testing** | Test different subject lines | Medium |
| 31 | **Personalization** | Advanced {{ name }}, {{ company }} | Small |
| 32 | **Visual Automation Builder** | Drag-and-drop sequences | Large |

---

## Email Template Variables

| Variable | Example |
|----------|---------|
| `{{ first_name }}` | Hi Sarah |
| `{{ last_name }}` | Smith |
| `{{ email }}` | sarah@example.com |
| `{{ product_name }}` | Cool Girl Rehab |
| `{{ purchase_date }}` | March 27, 2026 |
| `{{ unsubscribe_url }}` | /unsubscribe/abc123 |
| `{{ logo_url }}` | https://.../logo.png |
| `{{ brand_name }}` | Cool Girl Rehab |
| `{{ social_links }}` | Instagram, Facebook links |
| `{{ company_address }}` | 123 Main St, City |
| `{{ current_year }}` | 2026 |
| `{{ content }}` | Main email body content |

---

## Email Template Structure (What We're Building)

```html
<!DOCTYPE html>
<html>
<head>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700" rel="stylesheet">
    <style>
        body { font-family: 'Inter', sans-serif; color: #222222; }
        .brand-color { color: #e93d3d; }
        .btn { background: #e93d3d; }
    </style>
</head>
<body>
    <div class="header">
        <img src="{{ logo_url }}" alt="{{ brand_name }}">
    </div>

    <div class="content">
        {{ content }}
    </div>

    <div class="footer">
        <p>{{ social_links }}</p>
        <p>{{ company_address }}</p>
        <p><a href="{{ unsubscribe_url }}">Unsubscribe</a></p>
        <p>&copy; {{ current_year }} {{ brand_name }}</p>
    </div>
</body>
</html>
```

---

## Current Status

- ✅ Email Settings configured
- ✅ Send Functions created (email_utils.py)
- ⏳ Connect Send Button to function (CURRENT STEP)
- ⏳ Branded templates (later)
- ⏳ Tracking (later)

---

## Current Step

### Step 3: Connect Send Button + Create Email Templates Folder

Update views.py to call send_broadcast_email() function when user clicks "Send Now"
