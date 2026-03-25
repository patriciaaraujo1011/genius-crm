import re

DISPOSABLE_DOMAINS = [
    'tempmail.com', 'guerrillamail.com', '10minutemail.com', 'mailinator.com',
    'throwaway.email', 'fakeinbox.com', 'trashmail.com', 'mailnesia.com',
    'temp-mail.org', 'getnada.com', 'mohmal.com', 'tempail.com',
    'dispostable.com', 'mailcatch.com', 'yopmail.com', 'sharklasers.com',
    'guerrillamailblock.com', 'spam4.me', 'grr.la', 'discard.email',
    'discardmail.com', 'spamgourmet.com', 'mintemail.com', 'mailnull.com',
    'e4ward.com', 'spamfree24.org', 'mytrashmail.com', 'jetable.org',
]

COMMON_TYPOS = {
    'gmial.com': 'gmail.com',
    'gmal.com': 'gmail.com',
    'gmai.com': 'gmail.com',
    'gmaiil.com': 'gmail.com',
    'gmaill.com': 'gmail.com',
    'gamil.com': 'gmail.com',
    'gmail.co': 'gmail.com',
    'gmail.cm': 'gmail.com',
    'gmail.om': 'gmail.com',
    'gmailcom.com': 'gmail.com',
    'yahooo.com': 'yahoo.com',
    'yaho.com': 'yahoo.com',
    'yahooo.co': 'yahoo.com',
    'yhaoo.com': 'yahoo.com',
    'yahoo.co.uk': 'yahoo.com',
    'yahoo.com.au': 'yahoo.com',
    'hotmial.com': 'hotmail.com',
    'hotmial.co': 'hotmail.com',
    'hotmil.com': 'hotmail.com',
    'hotmai.com': 'hotmail.com',
    'hotmal.com': 'hotmail.com',
    'hotmail.co': 'hotmail.com',
    'hotmail.cm': 'hotmail.com',
    'hotmail.om': 'hotmail.com',
    'outloo.com': 'outlook.com',
    'outlok.com': 'outlook.com',
    'outloo.co': 'outlook.com',
    'outlook.co': 'outlook.com',
    'outlook.cm': 'outlook.com',
    'outlookcom.com': 'outlook.com',
    'msn.com': 'outlook.com',
    'msoutlook.com': 'outlook.com',
    'icloud.co': 'icloud.com',
    'i-cloud.com': 'icloud.com',
    'aol.co': 'aol.com',
    'aol.cm': 'aol.com',
    'aol.om': 'aol.com',
}


def validate_email(email):
    """
    Validate email address.
    Returns tuple: (is_valid, error_message)
    """
    if not email:
        return False, "Email is required"
    
    email = email.lower().strip()
    
    if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
        return False, "Please enter a valid email address"
    
    if ' ' in email:
        return False, "Email cannot contain spaces"
    
    if '@' not in email:
        return False, "Email must contain @ symbol"
    
    parts = email.split('@')
    if len(parts) != 2:
        return False, "Please enter a valid email address"
    
    local, domain = parts
    
    if not local or not domain:
        return False, "Please enter a valid email address"
    
    if local.startswith('.') or local.endswith('.'):
        return False, "Please enter a valid email address"
    
    if '..' in local:
        return False, "Please enter a valid email address"
    
    if domain.startswith('.') or domain.endswith('.'):
        return False, "Please enter a valid email address"
    
    if domain in DISPOSABLE_DOMAINS:
        return False, "Please use a permanent email address"
    
    if domain in COMMON_TYPOS:
        corrected = COMMON_TYPOS[domain]
        return False, f"Did you mean {corrected}?"
    
    return True, ""


def get_country_from_phone(phone):
    """
    Attempt to detect country from phone number prefix.
    Returns country name or empty string.
    """
    phone = re.sub(r'[\s\-\(\)]', '', phone)
    
    country_codes = {
        '1': 'United States/Canada',
        '44': 'United Kingdom',
        '61': 'Australia',
        '64': 'New Zealand',
        '65': 'Singapore',
        '852': 'Hong Kong',
        '853': 'Macau',
        '81': 'Japan',
        '82': 'South Korea',
        '86': 'China',
        '91': 'India',
        '62': 'Indonesia',
        '63': 'Philippines',
        '66': 'Thailand',
        '60': 'Malaysia',
        '1': 'United States',
    }
    
    for code, country in sorted(country_codes.items(), key=lambda x: -len(x[0])):
        if phone.startswith(code) and len(phone) > len(code):
            return country
    
    return ''
