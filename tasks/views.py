from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Task
from .serializers import TaskSerializer, TaskStatusUpdateSerializer, TaskDeleteSerializer

class TaskListCreateView(APIView):
  """
  View to list all tasks for the authenticated user and create a new task.
  """
  permission_classes = [IsAuthenticated]

  def get(self, request):
      """
      GET request to list all tasks for the authenticated user.
      
      Args:
        request: HTTP request object.
      
      Returns:
        Response: Serialized list of tasks for the user.
      """
      try:
        todos = Task.objects.filter(user=request.user, is_deleted=False)
        serializer = TaskSerializer(todos, many=True)
        return Response(serializer.data)
      except Exception as e:
        return Response(
          {"error": "An error occurred while retrieving tasks."},
          status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

  def post(self, request):
    """
    POST request to create a new task for the authenticated user.
    
    Args:
        request: HTTP request object containing new task data.
    
    Returns:
        Response: Serialized data of the created task, or validation errors.
    """
    serializer = TaskSerializer(data=request.data)
    if serializer.is_valid():
      try:
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
      except Exception as e:
        return Response(
          {"error": "An error occurred while saving the task."},
          status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskDetailView(APIView):
  """
  View to retrieve, update, or delete a specific task.
  """
  permission_classes = [IsAuthenticated]

  def get_object(self, pk, user):
      """
      Helper method to retrieve a task by ID for a specific user.
      
      Args:
        pk (str): Primary key of the task.
        user: The authenticated user requesting the task.
      
      Returns:
          Task: The task object if found, or None.
      """
      try:
        return Task.objects.get(id=pk, user=user, is_deleted=False)
      except Task.DoesNotExist:
        return None

  def get(self, request, pk):
    """
    GET request to retrieve a specific task.
    
    Args:
        request: HTTP request object.
        pk (int): Primary key of the task.
    
    Returns:
        Response: Serialized task data or a 404 not found error.
    """
    task = self.get_object(pk, request.user)
    if not task:
      return Response({"message": "Task not found."}, status=status.HTTP_404_NOT_FOUND)
    serializer = TaskSerializer(task)
    return Response(serializer.data)

  def post(self, request, pk):
    """
    POST request to partially update a specific task.
    
    Args:
      request: HTTP request object containing partial task data.
      pk (str): Primary key of the task.
    
    Returns:
      Response: Serialized updated task data or validation errors.
    """
    task = self.get_object(pk, request.user)
    if not task:
      return Response({"detail": "Task not found."}, status=status.HTTP_404_NOT_FOUND)
    serializer = TaskSerializer(task, data=request.data, partial=True)
    if serializer.is_valid():
      try:
        serializer.save()
        return Response(serializer.data)
      except Exception as e:
        return Response(
          {"error": "An error occurred while updating the task."},
          status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def delete(self, request, pk):
    """
    DELETE request to perform a soft delete on a specific task.
    
    Args:
      request: HTTP request object.
      pk (str): Primary key of the task.
    
    Returns:
      Response: Confirmation of deletion or 404 error if not found.
    """
    task = self.get_object(pk, request.user)
    if not task:
        return Response({"detail": "Task not found."}, status=status.HTTP_404_NOT_FOUND)
    
    # Soft-delete: set the is_deleted flag to True.
    serializer = TaskDeleteSerializer(task, data={"is_deleted": True})
    if serializer.is_valid():
      try:
        serializer.save()
        return Response(serializer.data)
      except Exception as e:
        return Response(
          {"error": "An error occurred while deleting the task."},
          status=status.HTTP_500_INTERNAL_SERVER_ERROR
          )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskStatusUpdateView(APIView):
  """
  View to update the status of a specific task.
  """
  permission_classes = [IsAuthenticated]

  def post(self, request, pk):
    """
    POST request to update the status of a specific task.
    
    Args:
      request: HTTP request object containing the new status.
      pk (str): Primary key of the task.
    
    Returns:
      Response: Updated task data or a 404 not found error.
    """
    try:
      task = Task.objects.get(id=pk, user=request.user)
    except Task.DoesNotExist:
      return Response({"detail": "Task not found."}, status=status.HTTP_404_NOT_FOUND)
      
    serializer = TaskStatusUpdateSerializer(task, data=request.data, partial=True)
    if serializer.is_valid():
      try:
        serializer.save()
        return Response(serializer.data)
      except Exception as e:
        return Response(
          {"error": "An error occurred while updating the task status."},
          status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BulkUpdateTaskStatusView(APIView):
  """
  API endpoint to bulk update the status of multiple tasks for the authenticated user.
  """
  permission_classes = [IsAuthenticated]

  def post(self, request):
      """
      POST request to bulk update task statuses.
      
      Args:
        request: HTTP request object containing 'task_ids' and 'status'.
      
      Returns:
        Response: Summary of update results.
      """
      task_ids = request.data.get("task_ids")
      status_to_update = request.data.get("status")

      # Validate request data
      if not task_ids or not isinstance(task_ids, list):
        return Response(
          {"error": "Invalid input. 'task_ids' must be a list of task IDs."},
          status=status.HTTP_400_BAD_REQUEST
        )

      if not status_to_update:
        return Response(
          {"error": "Missing 'status' field. Provide a status to update tasks."},
          status=status.HTTP_400_BAD_REQUEST
        )

      # Retrieve tasks
      user_tasks = Task.objects.filter(user=request.user, id__in=task_ids, is_deleted=False)
      updated_count, ignored_count = 0, len(task_ids) - user_tasks.count()
      errors = []

      for task in user_tasks:
        try:
          task.status = status_to_update
          task.save()
          updated_count += 1
        except Exception as e:
          errors.append({"task_id": task.id, "error": str(e)})

      response_data = {
        "updated_count": updated_count,
        "ignored_count": ignored_count,
        "errors": errors
      }

      return Response(response_data, status=status.HTTP_200_OK)


class BulkDeleteTasksView(APIView):
  """
  API endpoint to bulk delete multiple tasks for the authenticated user.
  """
  permission_classes = [IsAuthenticated]

  def delete(self, request):
      """
      DELETE request to perform a bulk soft-delete on tasks.
      
      Args:
        request: HTTP request object containing 'task_ids'.
      
      Returns:
        Response: Summary of deletion results.
      """
      task_ids = request.data.get("task_ids")

      # Validate request data
      if not task_ids or not isinstance(task_ids, list):
        return Response(
          {"error": "Invalid input. 'task_ids' must be a list of task IDs."},
          status=status.HTTP_400_BAD_REQUEST
        )

      user_tasks = Task.objects.filter(user=request.user, id__in=task_ids, is_deleted=False)
      updated_count, ignored_count = 0, len(task_ids) - user_tasks.count()
      errors = []

      for task in user_tasks:
        try:
          task.is_deleted = True
          task.save()
          updated_count += 1
        except Exception as e:
            errors.append({"task_id": task.id, "error": str(e)})

      response_data = {
        "updated_count": updated_count,
        "ignored_count": ignored_count,
        "errors": errors
      }

      return Response(response_data, status=status.HTTP_200_OK)
