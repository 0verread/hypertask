from django.urls import path
from .views import TodoListCreateView, TodoDetailView, TodoStatusUpdateView, BulkUpdateTaskStatusView, BulkDeleteTasksView

urlpatterns = [
  path('tasks', TodoListCreateView.as_view(), name='todo-list-create'), # List and create tasks
  path('tasks/bulk-update-status', BulkUpdateTaskStatusView.as_view(), name='bulk-update-task-status'), # Bulk status update
  path('tasks/bulk-delete', BulkDeleteTasksView.as_view(), name='bulk-delete-tasks'), # Bulk delete tasks
  path('tasks/<str:pk>', TodoDetailView.as_view(), name='todo-detail'), # Retrieve, update, and delete a Task
  path('tasks/<str:pk>/status', TodoStatusUpdateView.as_view(), name='todo-status-update'), # Update Todo status
]
