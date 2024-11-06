from django.urls import path
from .views import TodoListCreateView, TodoDetailView, TodoStatusUpdateView

urlpatterns = [
  path('', TodoListCreateView.as_view(), name='todo-list-create'), # List and create Todos
  path('<str:pk>', TodoDetailView.as_view(), name='todo-detail'), # Retrieve, update, and delete a Todo
  path('<str:pk>/status', TodoStatusUpdateView.as_view(), name='todo-status-update'), # Update Todo status
]
