from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def send_html_email(
    subject, html_content, recipient_list, from_email=None, attachments=None
):
    """
    Send an HTML email with optional attachments.

    Args:
        subject: Email subject line
        html_content: HTML content of the email
        recipient_list: List of email addresses
        from_email: Sender email (defaults to settings.DEFAULT_FROM_EMAIL)
        attachments: List of tuples (filename, content, mimetype)
    """
    if from_email is None:
        from_email = getattr(
            settings, "DEFAULT_FROM_EMAIL", "noreply@coolgirlrehab.com"
        )

    # Create plain text version from HTML
    plain_message = strip_tags(html_content)

    # Create email
    email = EmailMultiAlternatives(
        subject=subject,
        body=plain_message,
        from_email=from_email,
        to=recipient_list,
    )

    # Attach HTML version
    email.attach_alternative(html_content, "text/html")

    # Add attachments
    if attachments:
        for filename, content, mimetype in attachments:
            email.attach(filename, content, mimetype)

    # Send
    email.send(fail_silently=False)


def send_broadcast_email(broadcast, segment="all"):
    """
    Send a broadcast email to contacts in the specified segment.

    Args:
        broadcast: Broadcast model instance
        segment: 'all', 'active', 'at_risk', 'trial', or tag name
    """
    from crm.models import Contact

    # Get contacts based on segment
    if segment == "all":
        contacts = Contact.objects.all()
    elif segment == "active":
        contacts = Contact.objects.filter(is_buyer=True)
    elif segment == "at_risk":
        # Contacts with no activity in 30 days
        from datetime import timedelta

        from django.utils import timezone

        thirty_days_ago = timezone.now() - timedelta(days=30)
        contacts = Contact.objects.filter(last_activity__lt=thirty_days_ago)
    elif segment == "trial":
        contacts = Contact.objects.filter(tags__contains=["trial"])
    else:
        # Assume it's a tag
        contacts = Contact.objects.filter(tags__contains=[segment])

    # Get email addresses
    recipient_list = list(contacts.values_list("email", flat=True))

    if not recipient_list:
        return 0

    # Render HTML content using template
    context = {
        "subject": broadcast.subject,
        "message": broadcast.message,
        "brand_name": "Cool Girl Rehab",
        "logo_url": getattr(settings, "EMAIL_LOGO_URL", ""),
        "current_year": "2026",
        "company_address": getattr(settings, "EMAIL_COMPANY_ADDRESS", ""),
        "social_links": getattr(settings, "EMAIL_SOCIAL_LINKS", ""),
        "unsubscribe_url": getattr(
            settings, "EMAIL_UNSUBSCRIBE_URL", "/unsubscribe/"
        ),
        "preferences_url": getattr(
            settings, "EMAIL_PREFERENCES_URL", "/preferences/"
        ),
        "cta_url": "",
        "cta_text": "",
        "signature": "",
    }

    try:
        html_content = render_to_string("emails/broadcast.html", context)
    except Exception:
        # Fallback if template not found
        html_content = f"""
        <html>
        <body>
            <h1>{broadcast.subject}</h1>
            <p>{broadcast.message}</p>
            <p><a href="{context["unsubscribe_url"]}">Unsubscribe</a></p>
        </body>
        </html>
        """

    # Send
    send_html_email(
        subject=broadcast.subject,
        html_content=html_content,
        recipient_list=recipient_list,
    )

    # Update broadcast status to sent
    broadcast.status = "sent"
    broadcast.save(update_fields=["status", "sent_at"])

    return len(recipient_list)
