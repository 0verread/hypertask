import random
import string

def generate_custom_user_id(prefix="usr_", length=10):
  """Generate a custom ID with a specified prefix and random suffix."""
  suffix = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
  return f"{prefix}{suffix}"

def generate_custom_task_id(prefix='tsk_', length=12):
  """Generate a custom ID with a specified prefix and random suffix."""
  suffix = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
  return f"{prefix}{suffix}"
