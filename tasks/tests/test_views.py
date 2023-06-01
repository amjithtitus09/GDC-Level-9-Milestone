from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model

from tasks.models import Task
from ..views import TaskListView, UserUpdateView, TaskCreateView, TaskDeleteView, TaskDetailView, \
    TaskCompleteView, TaskUpdateView, CompletedTaskListView, send_reports
User = get_user_model()

class FunctionTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username="amjithtitus09", email="amjithtitus09@gmail.com", password="ascii123")

class UserSignUpViewTest(TestCase):
    def test_get(self):

        response = self.client.get("/user/signup")
        self.assertEqual(response.status_code, 200)

class UserLoginViewTest(TestCase):
    def test_get(self):

        response = self.client.get("/user/login")
        self.assertEqual(response.status_code, 200)

class TaskListViewTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username="amjithtitus09", email="amjithtitus09@gmail.com", password="ascii123")

    def test_get(self):

        request = self.factory.get("/tasks/")
        request.user = self.user
        self.assertEqual(TaskListView.as_view()(request).status_code, 200)


class UserUpdateViewTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username="amjithtitus09", email="amjithtitus09@gmail.com", password="ascii123")

    def test_get(self):

        request = self.factory.get("/tasks/")
        request.user = self.user
        self.assertEqual(UserUpdateView.as_view()(request, pk = self.user.pk).status_code, 200)

class TaskCreateViewTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username="amjithtitus09", email="amjithtitus09@gmail.com", password="ascii123")

    def test_get(self):
        request = self.factory.get('/create-task/')
        request.user = self.user
        response = TaskCreateView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_post(self):
        
        data = {
                    'title': 'Title Title Title Title ',
                    'description': 'Title Title Title Title ',
                    'priority': '1',
                    'status': 'PENDING',
                    'user': self.user
                }

        request = self.factory.post( '/create-task/', data=data)
        request.user = self.user
        response = TaskCreateView.as_view()(request)
        self.assertEqual(Task.objects.last().title, 'TITLE TITLE TITLE TITLE')


class TaskUpdateViewTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username="amjithtitus09", email="amjithtitus09@gmail.com", password="ascii123")
        self.task = Task.objects.create(title="Title Title Title Title", description="Title Title Title Title", \
                                             priority=1, status= "PENDING", user = self.user)

    def test_get(self):
        request = self.factory.get('/update-task/')
        request.user = self.user
        response = TaskUpdateView.as_view()(request, pk = self.task.pk)
        self.assertEqual(response.status_code, 200)

    def test_post(self):
        data = {
                    'title': 'Title Title Title Title ',
                    'description': 'New description',
                    'priority': '1',
                    'status': 'PENDING',
                    'user': self.user
                }
        

        request = self.factory.post( '/update-task/', data=data)
        request.user = self.user
        response = TaskUpdateView.as_view()(request, pk = self.task.pk)
        self.assertEqual(Task.objects.get(pk = self.task.pk).description, 'New description')

class TaskDeleteViewTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username="amjithtitus09", email="amjithtitus09@gmail.com", password="ascii123")
        self.task = Task.objects.create(title="Title Title Title Title", description="Title Title Title Title", \
                                             priority=1, status= "PENDING", user = self.user)

    def test_delete(self):

        request = self.factory.delete( '/delete-task/')
        request.user = self.user
        response = TaskDeleteView.as_view()(request, pk = self.task.pk)
        self.assertEqual(Task.objects.filter(pk = self.task.pk).count(), 0)


class TaskCompleteViewTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username="amjithtitus09", email="amjithtitus09@gmail.com", password="ascii123")
        self.task = Task.objects.create(title="Title Title Title Title", description="Title Title Title Title", \
                                             priority=1, status= "PENDING", user = self.user)

    def test_post(self):
        data = {
                    'title': 'Title Title Title Title ',
                    'description': 'New description',
                    'priority': '1',
                    'status': 'COMPLETED',
                    'user': self.user
                }
        

        request = self.factory.post( '/complete_task/', data=data)
        request.user = self.user
        response = TaskCompleteView.as_view()(request, pk = self.task.pk)
        self.assertEqual(Task.objects.get(pk = self.task.pk).status, 'COMPLETED')


class TaskDetailViewTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username="amjithtitus09", email="amjithtitus09@gmail.com", password="ascii123")
        self.task = Task.objects.create(title="Title Title Title Title", description="Title Title Title Title", \
                                             priority=1, status= "PENDING", user = self.user)

    def test_get(self):

        request = self.factory.get( '/complete_task/')
        request.user = self.user
        response = TaskDetailView.as_view()(request, pk = self.task.pk)
        self.assertEqual(response.status_code, 200)

class CompletedTaskListViewTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username="amjithtitus09", email="amjithtitus09@gmail.com", password="ascii123")
        self.task = Task.objects.create(title="Title Title Title Title", description="Title Title Title Title", \
                                             priority=1, status= "COMPLETED", user = self.user)

    def test_get(self):

        request = self.factory.get( '/completed_tasks/')
        request.user = self.user
        response = CompletedTaskListView.as_view()(request)
        self.assertEqual(response.status_code, 200)

import datetime
from django.db.models import Q
class CelerySendReportsTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username="amjithtitus09", email="amjithtitus09@gmail.com", password="ascii123")
        self.task = Task.objects.create(title="Title Title Title Title", description="Title Title Title Title", \
                                             priority=1, status= "COMPLETED", user = self.user)

    def test_get(self):
        self.user.send_report_at=datetime.datetime.today()
        self.user.save()
        before_count = User.objects.filter(send_report_at__isnull=False, send_report_at__lte=datetime.datetime.now().time()).filter(Q(last_sent_on__isnull=True) | Q(last_sent_on__lt=datetime.datetime.today())).count()
        send_reports()
        after_count = User.objects.filter(send_report_at__isnull=False, send_report_at__lte=datetime.datetime.now().time()).filter(Q(last_sent_on__isnull=True) | Q(last_sent_on__lt=datetime.datetime.today())).count()
        self.assertEqual(before_count - after_count, 1)