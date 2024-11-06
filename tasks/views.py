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