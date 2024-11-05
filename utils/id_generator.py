import random
import string

def generate_custom_id(prefix, length):
  """Generate a custom ID with a specified prefix and random suffix."""
  suffix = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
  return f"{prefix}{suffix}"
