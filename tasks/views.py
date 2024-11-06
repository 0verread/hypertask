from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Task
from .serializers import TaskSerializer, TaskStatusUpdateSerializer, TaskDeleteSerializer

class TodoListCreateView(APIView):
  """
  View to list all Todos for the authenticated user and create a new Todo.
  """
  permission_classes = [IsAuthenticated]

  def get(self, request):
      """List all tasks ( that are not deleted) for the authenticated user"""
      todos = Task.objects.filter(user=request.user).filter(is_deleted=False)
      serializer = TaskSerializer(todos, many=True)
      return Response(serializer.data)

  def post(self, request):
      """Create a new todo for the authenticated user"""
      serializer = TaskSerializer(data=request.data)
      if serializer.is_valid():
          serializer.save(user=request.user)
          return Response(serializer.data, status=status.HTTP_201_CREATED)
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TodoDetailView(APIView):
    """
    View to retrieve, update, or delete a specific Todo item.
    """
    permission_classes = [IsAuthenticated]

    def get_object(self, pk, user):
        """Helper method to get task object"""
        try:
            return Task.objects.get(id=pk, user=user, is_deleted=False)
        except Task.DoesNotExist:
            return None

    def get(self, request, pk):
      """Retrieve a specific task"""
      task = self.get_object(pk, request.user)
      if not task:
        return Response(
          {"message": "Task not found."}, 
          status=status.HTTP_404_NOT_FOUND
        )
      serializer = TaskSerializer(task)
      return Response(serializer.data)

    def put(self, request, pk):
        """Update a specific task"""
        todo = self.get_object(pk, request.user)
        if not todo:
            return Response(
              {"message": "Todo not found."}, 
              status=status.HTTP_404_NOT_FOUND
            )
        serializer = TaskSerializer(todo, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        """Partially update a specific todo"""
        todo = self.get_object(pk, request.user)
        if not todo:
            return Response(
                {"detail": "Todo not found."}, 
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = TaskSerializer(todo, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
      """Delete a specific task"""
      task = self.get_object(pk, request.user)
      if not task:
        return Response(
          {"detail": "task not found."}, 
          status=status.HTTP_404_NOT_FOUND
        )
      
      """
      we perform soft-delete (i.e. set is_deleted flag True).
      this is for internal data analytics, data recovery and many more
      """
      serializer = TaskDeleteSerializer(task, data={"is_deleted": True})
      if serializer.is_valid():
         serializer.save()
         return Response(serializer.data)
      return Response(status=status.HTTP_204_NO_CONTENT)

class TodoStatusUpdateView(APIView):
  """
  View to update the status of a specific Task item.
  """
  permission_classes = [IsAuthenticated]

  def patch(self, request, pk):
    try:
      task = Task.objects.get(id=pk, user=request.user)
    except Task.DoesNotExist:
      return Response(
        {"detail": "Task not found."}, 
        status=status.HTTP_404_NOT_FOUND
      )

    serializer = TaskStatusUpdateSerializer(task, data=request.data, partial=True)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  

class BulkUpdateTaskStatusView(APIView):
    """
    API endpoint to bulk update the status of multiple tasks for the authenticated user.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
      """
      POST request to update the status of multiple tasks.
      - Request body should contain 'task_ids' (list of task IDs) and 'status'.
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

      # Retrieve tasks belonging to the user from the provided task_ids
      user_tasks = Task.objects.filter(user=request.user, id__in=task_ids, is_deleted=False)

      # Perform the update for valid tasks
      updated_count = 0
      ignored_count = len(task_ids) - user_tasks.count()
      errors = []

      for task in user_tasks:
          try:
              task.status = status_to_update
              task.save()
              updated_count += 1
          except Exception as e:
              # Collect any errors encountered during the update
              errors.append({"task_id": task.id, "error": str(e)})

      # Construct the response
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
      POST request to update the status of multiple tasks.
      - Request body should contain 'task_ids' (list of task IDs).
      """
      task_ids = request.data.get("task_ids")

      # Validate request data
      if not task_ids or not isinstance(task_ids, list):
          return Response(
              {"error": "Invalid input. 'task_ids' must be a list of task IDs."},
              status=status.HTTP_400_BAD_REQUEST
          )

      # Retrieve tasks belonging to the user from the provided task_ids
      user_tasks = Task.objects.filter(user=request.user, id__in=task_ids, is_deleted=False)

      # Perform the update for valid tasks
      updated_count = 0
      ignored_count = len(task_ids) - user_tasks.count()
      errors = []

      for task in user_tasks:
          try:
              task.is_deleted = True
              task.save()
              updated_count += 1
          except Exception as e:
              # Collect any errors encountered during the update
              errors.append({"task_id": task.id, "error": str(e)})

      # Construct the response
      response_data = {
          "updated_count": updated_count,
          "ignored_count": ignored_count,
          "errors": errors
      }

      return Response(response_data, status=status.HTTP_200_OK)

