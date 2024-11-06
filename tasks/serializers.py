from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
  """
  Serializer for creating, retrieving, and updating Todo items.
  """
  class Meta:
    model = Task
    fields = ["id", "title", "description", "status", "created_at", "updated_at"]
    read_only_fields = ["id", "created_at", "updated_at"]

class TaskStatusUpdateSerializer(serializers.ModelSerializer):
  """
  Serializer for updating only the status of a Todo item.
  """

  class Meta:
    model = Task
    fields = ["status"]

class TaskDeleteSerializer(serializers.ModelSerializer):
  """
  Serializer for Deleting Task item.
  """

  class Meta:
    model = Task
    fields = ["is_deleted"]
