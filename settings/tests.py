from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import views


class PasswordChangeTests(TestCase):

    def setUp(self):
        username = 'admin'
        password = 'personal@124'
        User.objects.create_user(username=username, email='admin@gmail.com', password=password)

        url = reverse('settings:password_change')
        self.client.login(username=username, password=password)
        self.response = self.client.get(url)

    def test_password_change_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_password_change_resolve_function(self):
        view = resolve('/settings/password/')
        self.assertEqual(view.func.view_class, views.PasswordChangeView)

    def test_password_change_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_password_change_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, PasswordChangeForm)

    def test_password_change_form_inputs(self):
        """The view must contain four inputs: csrf, old_password, new_password1, new_password2"""
        self.assertContains(self.response, '<input', 4)
        self.assertContains(self.response, 'type="password"', 3)


class LoginRequiredPasswordChangeTests(TestCase):

    def test_redirection(self):
        url = reverse('settings:password_change')
        login_url = reverse('accounts:login')
        response = self.client.get(url)
        self.assertRedirects(response, f'{login_url}?next={url}')


class PasswordChangeTestCase(TestCase):
    """Base test case for form processing accepts a 'data' dict to POST to the view"""
    def setUp(self, data={}):
        self.user = User.objects.create_user(username='admin', email='admin@gmail.com', password='old_password')
        self.url = reverse('settings:password_change')
        self.client.login(username='admin', password='old_password')
        self.response = self.client.post(self.url, data)


class SuccessfulPasswordChangeTests(PasswordChangeTestCase):

    def setUp(self):
        super().setUp({
            'old_password': 'old_password',
            'new_password1': 'new_password',
            'new_password2': 'new_password'
        })

    def test_redirection(self):
        """A valid form submission should redirect the user"""
        self.assertRedirects(self.response, reverse('settings:password_change_done'))

    def test_password_changed(self):
        """Refresh the user instance from database to get the new password hash updated by the change password view"""
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('new_password'))

    def test_user_authentication(self):
        """Create a new request to an arbitrary page. The resulting response should now have an 'user' to its context,
        after a successful sign up"""
        response = self.client.get(reverse('tutorial:index'))
        user = response.context.get('user')
        self.assertTrue(user.is_authenticated)


class InvalidPasswordChangeTests(PasswordChangeTestCase):

    def test_status_code(self):
        """An invalid form submission should return to the same page"""
        self.assertEqual(self.response.status_code, 200)

    def test_form_errors(self):
        form = self.response.context.get('form')
        self.assertTrue(form.errors)

    def test_did_not_change_password(self):
        """Refresh the user instance from the database to make sure we have the latest data"""
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('old_password'))
