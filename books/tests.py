from django.test import TestCase
from . forms import LoginForm


class ProjectTests(TestCase):

    def test_basepage_without_cookie(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 302)

    def test_loginpage(self):
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 200)

    def test_loginform(self):
        form_data = {'email': 'example@gmail.com', 'password': 'some string'}
        form = LoginForm(data=form_data)
        self.assertTrue(form.is_valid())
