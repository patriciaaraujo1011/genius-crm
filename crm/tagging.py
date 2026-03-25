"""
Lead Tagging Utility
Reusable functions for automatically tagging leads from any opt-in form.

Usage:
    from crm.tagging import get_lead_tags

    tags = get_lead_tags(
        request=request,
        template_name='opt-in-1',
        slug='my-funnel',
        lead_type='lead-magnet'
    )
"""

from datetime import datetime


def get_lead_tags(
    request, template_name="opt-in-1", slug=None, lead_type="lead-magnet"
):
    """
    Generate automatic tags for a lead based on request and parameters.

    Args:
        request: Django request object (for UTM parameters)
        template_name: Name/number of the opt-in template (e.g., 'opt-in-1')
        slug: Funnel slug (optional)
        lead_type: Type of lead magnet (e.g., 'lead-magnet', 'webinar', 'free-trial')

    Returns:
        list: List of tags to apply to the contact
    """
    tags = []

    tags.append(template_name)

    if slug:
        tags.append(slug)
    else:
        tags.append("main")

    utm_source = request.GET.get("utm_source", "")
    utm_medium = request.GET.get("utm_medium", "")
    utm_campaign = request.GET.get("utm_campaign", "")

    source = utm_source or request.POST.get("source", "organic")
    if not source or source == "organic":
        if utm_medium:
            source = utm_medium
        else:
            source = "organic"

    tags.append(source)

    tags.append(datetime.now().strftime("%B-%Y").lower())

    tags.append(lead_type)

    if utm_campaign:
        tags.append(f"campaign-{utm_campaign}")

    if utm_source:
        tags.append(f"source-{utm_source}")

    return tags


def get_utm_data(request):
    """
    Extract UTM parameters from request.

    Returns:
        dict: UTM data with keys: utm_source, utm_medium, utm_campaign, utm_content, utm_term
    """
    return {
        "utm_source": request.GET.get("utm_source", ""),
        "utm_medium": request.GET.get("utm_medium", ""),
        "utm_campaign": request.GET.get("utm_campaign", ""),
        "utm_content": request.GET.get("utm_content", ""),
        "utm_term": request.GET.get("utm_term", ""),
    }


def apply_tags_to_contact(contact, tags):
    """
    Apply tags to a contact, avoiding duplicates.

    Args:
        contact: Contact model instance
        tags: List of tags to add
    """
    for tag in tags:
        if tag not in contact.tags:
            contact.tags.append(tag)
    contact.save()
