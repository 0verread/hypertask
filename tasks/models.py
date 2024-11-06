from django.db import models
from users.models import CustomUser

from .enums import TaskStatus
from utils.id_generator import generate_custom_task_id


class Task(models.Model):
  id = models.CharField(max_length=16, primary_key=True, editable=False, default= generate_custom_task_id)
  user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="tasks")
  title = models.CharField(max_length=255)
  description = models.TextField(blank=True)
  status = models.CharField(max_length=20, choices=[(status.value, status.value) for status in TaskStatus], default=TaskStatus.PENDING.value)
  is_deleted = models.BooleanField(default=False)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
      return f"{self.title} - {self.status}"

  class Meta:
    db_table = 'tasks'

