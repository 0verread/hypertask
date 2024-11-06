from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import Task
from django.contrib.auth import get_user_model

User = get_user_model()


class TaskTests(TestCase):
  def setUp(self):
    """Set up the test client and create a user and a task for testing."""
    self.client = APIClient()
    self.user = User.objects.create_user(email="testuser@gmail.com", password="testpassword")
    self.client.force_authenticate(user=self.user)
    self.task = Task.objects.create(
      user=self.user,
      title="Test Task",
      description="A test task description",
      status="pending"
    )

  def test_list_tasks(self):
    """Test listing all tasks for an authenticated user."""
    url = reverse('task-list-create')
    response = self.client.get(url)
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertGreater(len(response.data), 0)  # Ensure at least one task is returned

  def test_create_task(self):
    """Test creating a new task."""
    url = reverse('task-list-create')
    data = {
      "title": "New Task",
      "description": "Description for the new task"
    }
    response = self.client.post(url, data)
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    self.assertEqual(response.data['title'], data['title'])

  def test_get_task_detail(self):
    """Test retrieving a single task detail."""
    url = reverse('task-detail', args=[self.task.id])
    response = self.client.get(url)
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(response.data['title'], self.task.title)

  def test_update_task(self):
    """Test updating a task with PUT."""
    url = reverse('task-detail', args=[self.task.id])
    data = {
      "title": "Updated Task Title",
      "description": self.task.description,
      "status": "COMPLETED"
    }
    response = self.client.put(url, data)
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.task.refresh_from_db()
    self.assertEqual(self.task.title, "Updated Task Title")

  def test_partial_update_task(self):
    """Test partially updating a task with PATCH."""
    url = reverse('task-detail', args=[self.task.id])
    data = {"title": "Partially Updated Title"}
    response = self.client.patch(url, data)
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.task.refresh_from_db()
    self.assertEqual(self.task.title, "Partially Updated Title")

  def test_delete_task(self):
    """Test soft-deleting a task."""
    url = reverse('task-detail', args=[self.task.id])
    response = self.client.delete(url)
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.task.refresh_from_db()
    self.assertTrue(self.task.is_deleted)

  def test_bulk_update_task_status(self):
    """Test bulk updating task statuses."""
    # Create additional tasks for bulk updating
    task2 = Task.objects.create(user=self.user, title="Task 2")
    url = reverse('bulk-update-task-status')
    data = {
        "task_ids": [self.task.id, task2.id],
        "status": "COMPLETED"
    }
    response = self.client.post(url, data, format='json')
    print(response)
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.task.refresh_from_db()
    task2.refresh_from_db()
    self.assertEqual(self.task.status, "COMPLETED")
    self.assertEqual(task2.status, "COMPLETED")

  def test_bulk_delete_tasks(self):
    """Test bulk soft-deleting tasks."""
    # Create additional tasks for bulk deleting
    task2 = Task.objects.create(user=self.user, title="Task 2", status="pending")
    url = reverse('bulk-delete-tasks')
    data = {"task_ids": [self.task.id, task2.id]}
    response = self.client.delete(url, data, format='json')
    print(response)
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.task.refresh_from_db()
    task2.refresh_from_db()
    self.assertTrue(self.task.is_deleted)
    self.assertTrue(task2.is_deleted)

  def test_update_task_status(self):
    """Test updating the status of a single task."""
    url = reverse('task-status-update', args=[self.task.id])
    data = {"status": "COMPLETED"}
    response = self.client.patch(url, data)
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.task.refresh_from_db()
    self.assertEqual(self.task.status, "COMPLETED")

  def test_get_task_not_found(self):
    """Test retrieving a non-existing task."""
    url = reverse('task-detail', args=[9999])  # Assuming task with ID 9999 does not exist
    response = self.client.get(url)
    self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

  def test_update_task_not_found(self):
    """Test updating a non-existing task."""
    url = reverse('task-detail', args=[9999])  # Assuming task with ID 9999 does not exist
    data = {"title": "Non-existing task update"}
    response = self.client.put(url, data)
    self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

