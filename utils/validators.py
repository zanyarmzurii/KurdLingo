import re

def is_valid_phone(phone: str) -> bool:
    """Check if a string looks like a valid international phone number."""
    pattern = r'^\+?[1-9]\d{1,14}$'
    return bool(re.match(pattern, phone))

def is_valid_username(username: str) -> bool:
    """Telegram usernames are 5-32 chars, alphanumeric + underscore."""
    pattern = r'^[a-zA-Z0-9_]{5,32}$'
    return bool(re.match(pattern, username))
