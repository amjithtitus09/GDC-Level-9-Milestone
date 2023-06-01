from django.test import TestCase
from rest_framework.test import APIRequestFactory
from django.contrib.auth import get_user_model
from rest_framework.test import force_authenticate
from tasks.apiviews import TaskViewSet

from tasks.models import Task

User = get_user_model()

class TaskViewSetTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="amjithtitus09", email="amjithtitus09@gmail.com", password="ascii123")
        self.task = Task.objects.create(title="Title Title Title Title", description="Title Title Title Title", \
                                             priority=1, status= "PENDING", user = self.user)

    def test_get_list(self):
        factory = APIRequestFactory()
        request = factory.get('/api/task/')
        force_authenticate(request, user=self.user)
        view = TaskViewSet.as_view({
            'get': 'list',
            'get': 'retrieve',
            'put': 'update',
            'patch': 'partial_update',
            'delete': 'destroy'
        })
        response = view(request, pk = self.task.pk)
        self.assertEqual(response.status_code, 200)
