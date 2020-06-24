from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordResetForm
from .. import views
from django.core import mail


class PasswordResetTests(TestCase):

    def setUp(self):
        url = reverse('accounts:password_reset')
        self.response = self.client.get(url)

    def test_password_reset_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_password_reset_view_resolves(self):
        view = resolve('/accounts/reset/')
        self.assertEqual(view.func.view_class, views.CustomPasswordResetView)

    def test_password_reset_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_password_reset_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, PasswordResetForm)

    def test_password_reset_form_inputs(self):
        """The view must contain two inputs: csrf and email"""
        self.assertContains(self.response, '<input', 2)
        self.assertContains(self.response, 'type="email"', 1)


class SuccessfulPasswordResetTests(TestCase):

    def setUp(self):
        email = "admin@gmail.com"
        User.objects.create_user(username='admin', email=email, password='personal@124')
        url = reverse('accounts:password_reset')
        self.response = self.client.post(url, {'email': email})

    def test_password_reset_redirection(self):
        """A valid form submission should redirect the user to 'password_reset_done'"""
        url = reverse('accounts:password_reset_done')
        self.assertRedirects(self.response, url)

    def test_send_password_reset_email(self):
        self.assertEqual(1, len(mail.outbox))


class InvalidPasswordResetTests(TestCase):

    def setUp(self):
        url = reverse('accounts:password_reset')
        self.response = self.client.post(url, {'email': 'donotexist@gmail.com'})

    def test_password_reset_redirection(self):
        """Even invalid email in the database should redirect the user to 'password_reset_done' view"""
        url = reverse('accounts:password_reset_done')
        self.assertRedirects(self.response, url)

    def test_no_reset_email_sent(self):
        self.assertEqual(0, len(mail.outbox))
