import random, string, json

def format_number(num: int) -> str:
    """Format integer with commas."""
    return f"{num:,}"

def generate_referral_code(length: int = 8) -> str:
    """Generate a random alphanumeric referral code."""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

def parse_json_safe(s: str, default=None):
    """Safely parse a JSON string."""
    try:
        return json.loads(s)
    except (json.JSONDecodeError, TypeError):
        return default
