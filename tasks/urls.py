from django.urls import path
from .views import TaskListCreateView, TaskDetailView, TaskStatusUpdateView, BulkUpdateTaskStatusView, BulkDeleteTasksView

urlpatterns = [
  path('tasks', TaskListCreateView.as_view(), name='todo-list-create'), # List and create tasks
  path('tasks/bulk-update-status', BulkUpdateTaskStatusView.as_view(), name='bulk-update-task-status'), # Bulk status update
  path('tasks/bulk-delete', BulkDeleteTasksView.as_view(), name='bulk-delete-tasks'), # Bulk delete tasks
  path('tasks/<str:pk>', TaskDetailView.as_view(), name='todo-detail'), # Retrieve, update, and delete a Task
  path('tasks/<str:pk>/status', TaskStatusUpdateView.as_view(), name='todo-status-update'), # Update Todo status
]
