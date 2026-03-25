# Lead Tagging System - Platform Convention

## Overview
All opt-in forms in the Genius CRM must automatically tag leads with standardized tags when they submit. This ensures consistent tracking and segmentation across all funnels.

---

## Automatic Tags Applied to Every Lead

When a lead submits any opt-in form, the following tags are **automatically** applied:

### 1. Template Tag
- **Format:** `opt-in-{number}` (e.g., `opt-in-1`, `opt-in-2`)
- **Purpose:** Identify which form template was used
- **How to set:** Update the template number in the view

### 2. Funnel Tag
- **Format:** Generated from funnel name, lowercase, underscores (e.g., `summer_sale_funnel`)
- **Purpose:** Identify which funnel the lead came from
- **Auto-updates:** When funnel name changes, tag updates automatically

### 3. Source Tag
- **Format:** Source name from UTM or default
- **Purpose:** Track where traffic came from
- **Sources:** `organic`, `facebook`, `instagram`, `google`, `tiktok`, `email`, etc.

### 4. Date Tag
- **Format:** `month-year` lowercase (e.g., `march-2026`)
- **Purpose:** Track when lead was captured

### 5. Lead Type Tag
- **Format:** `lead-magnet`, `webinar`, `free-trial`, etc.
- **Purpose:** Identify the offer type

### 6. UTM Tags (if available)
- **Format:** `campaign-{name}`, `source-{name}`
- **Purpose:** Track specific ad campaigns
- **Applied from:** URL parameters `utm_source`, `utm_medium`, `utm_campaign`

---

## View Code Pattern

All opt-in views must follow this pattern:

```python
from datetime import datetime

def optin_page(request, slug=None):
    if request.method == 'POST':
        # ... get form data ...
        
        # Capture UTM parameters
        utm_source = request.GET.get('utm_source', '')
        utm_medium = request.GET.get('utm_medium', '')
        utm_campaign = request.GET.get('utm_campaign', '')
        
        # Determine source from UTM or default
        source = request.POST.get('source', 'organic')
        if not source or source == 'organic':
            if utm_source:
                source = utm_source
        
        # Build tag list
        tags_to_add = [
            'opt-in-1',  # UPDATE: template tag
            slug or 'main',  # Funnel tag
            source,  # Source tag
            datetime.now().strftime('%B-%Y').lower(),  # Date tag
            'lead-magnet',  # Lead type tag
        ]
        
        # Add UTM-based tags
        if utm_campaign:
            tags_to_add.append(f'campaign-{utm_campaign}')
        if utm_source:
            tags_to_add.append(f'source-{utm_source}')
        
        # Create or update contact
        contact, created = Contact.objects.get_or_create(
            email=email,
            defaults={
                'first_name': first_name,
                'last_name': last_name,
                'phone': full_phone,
                'country': country,
                'source': source,
                'utm_source': utm_source,
                'utm_medium': utm_medium,
                'utm_campaign': utm_campaign,
                'tags': tags_to_add,
                'pipeline_stage': 'new_lead'
            }
        )
        
        # If contact exists, add new tags
        if not created:
            for tag in tags_to_add:
                if tag not in contact.tags:
                    contact.tags.append(tag)
            contact.save()
        
        return redirect('optin_thankyou')
```

---

## UTM URL Setup for Ads

When running Meta/Facebook ads, set the destination URL format:

```
https://yourdomain.com/opt-in/?utm_source=facebook&utm_medium=cpc&utm_campaign=your_campaign_name
```

### UTM Parameters Explained:
- **utm_source:** Where (facebook, instagram, google)
- **utm_medium:** How (cpc, social, email)
- **utm_campaign:** What (campaign name)
- **utm_content:** Which ad variant
- **utm_term:** Targeting keyword

---

## Source Choices (for Contact.source field)

When adding contacts manually or for reference:

- `organic` - Untracked traffic
- `facebook` - Facebook post/page
- `instagram` - Instagram
- `meta_ad` - Meta/Facebook paid ad
- `google_ad` - Google Ads
- `tiktok` - TikTok
- `email` - Email campaign
- `referral` - Word of mouth
- `webinar` - Webinar registration
- `lead_magnet_freebie_a` - First freebie
- `lead_magnet_freebie_b` - Second freebie
- `manual` - Manually added

---

## Example Tags for a Lead

**URL:** `/opt-in/?utm_source=facebook&utm_medium=cpc&utm_campaign=spring_sale_2026`

**Lead Tags:**
```python
[
    'opt-in-1',                    # Template
    'main',                        # Funnel
    'facebook',                    # Source
    'march-2026',                 # Date
    'lead-magnet',                # Lead type
    'campaign-spring_sale_2026',   # UTM campaign
    'source-facebook'              # UTM source
]
```

---

## Testing

To test tagging system:
```python
from crm.models import Contact
contacts = Contact.objects.order_by('-created_at')[:5]
for c in contacts:
    print(f"{c.first_name}: {c.tags}")
```

---

**Last Updated:** March 25, 2026
