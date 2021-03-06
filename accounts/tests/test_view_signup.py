from django.test import TestCase
from django.urls import reverse, resolve
from ..views import signup
from ..forms import SignUpForm
from django.contrib.auth.models import User


class SignUpTests(TestCase):

    def setUp(self):
        url = reverse('accounts:signup')
        self.response = self.client.get(url)

    def test_signup_view_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_signup_view_resolve(self):
        view = resolve('/accounts/signup/')
        self.assertEqual(view.func, signup)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_signup_view_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, SignUpForm)

    def test_form_inputs(self):
        """
        The view must contain five inputs:
        csrf, username, email, password1, password2
        """
        self.assertContains(self.response, '<input', 5)
        self.assertContains(self.response, 'type="text"', 1)
        self.assertContains(self.response, 'type="email"', 1)
        self.assertContains(self.response, 'type="password"', 2)


class SuccessfulSignUpTests(TestCase):

    def setUp(self):
        url = reverse('accounts:signup')
        data = {
            'username': 'admin',
            'email': 'admin@gmail.com',
            'password1': 'personal@124',
            'password2': 'personal@124'
        }
        self.response = self.client.post(url, data)
        self.home_url = reverse('tutorial:index')

    def test_redirection(self):
        """A valid form submission should redirect the user to the home page"""
        self.assertRedirects(self.response, self.home_url)

    def test_user_creation(self):
        self.assertTrue(User.objects.exists())

    def test_user_authentication(self):
        """
        Create a new request to an arbitrary page.
        The resulting response should now have a 'user' to its context
        after a successful sign up
        """
        response = self.client.get(self.home_url)
        user = response.context.get('user')
        self.assertTrue(user.is_authenticated)


class InvalidSignUpTests(TestCase):

    def setUp(self):
        url = reverse('accounts:signup')
        self.response = self.client.post(url, {})

    def test_signup_view_status_code(self):
        """An invalid form submission should return to the same page"""
        self.assertEqual(self.response.status_code, 200)

    def test_form_errors(self):
        form = self.response.context.get('form')
        self.assertTrue(form.errors)

    def test_do_not_create_users(self):
        self.assertFalse(User.objects.exists())
