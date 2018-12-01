from django.apps import apps
from django.conf import settings
from django.contrib.auth.models import Permission
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.shortcuts import resolve_url
from django.test import Client
from django.test import TestCase
from django.utils.functional import lazy
from selenium.webdriver.chrome.webdriver import WebDriver

from demo.models import Question

lazy_resolve_url = lazy(resolve_url, str)


class SeleniumTest(StaticLiveServerTestCase):
    client = None

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client = WebDriver()
        cls.client.implicity_wait(10)


class ClientMixin(object):
    client = None

    @classmethod
    def setUpClass(cls):
        cls.client = Client()

    def login_with_permissions(self, *perms):
        permissions = [
            Permission.objects.get(codename=p.split('.', 1)[1], content_type__app_label=p.split('.', 1)[0])
            for p in perms
        ]
        credential = dict(
            username="django_test",
            password="Pass@321",
        )
        auth_user_model = apps.get_model(getattr(settings, 'AUTH_USER_MODEL', 'auth.User'))
        user = auth_user_model.objects.create_user(**credential)
        user.user_permissions.add(*permissions)
        self.client.login(**credential)
        return user


class QuestionEmptySelectizeViewTest(TestCase, ClientMixin):
    list_url = lazy_resolve_url('selectize:selectize-demo-question')

    def test_list(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)

    def test_search(self):
        response = self.client.get(self.list_url, data=dict(q="term"))
        self.assertEqual(response.status_code, 200)

    def test_insert_without_permission(self):
        question_text = "new question"
        response = self.client.post(self.list_url, data=dict(
            q=question_text
        ))
        self.assertEqual(response.status_code, 403)
        questions = Question.objects.all()
        self.assertEqual(len(questions), 0)

    def test_insert(self):
        self.login_with_permissions("demo.add_question")
        question_text = "new question"
        response = self.client.post(self.list_url, data=dict(
            q=question_text
        ))
        self.assertEqual(response.status_code, 201)
        questions = Question.objects.all()
        self.assertEqual(len(questions), 1)
        self.assertEqual(questions[0].text, question_text)


class QuestionSelectizeViewTest(TestCase, ClientMixin):
    pass


class TestPollSelectizeView(TestCase):
    pass
