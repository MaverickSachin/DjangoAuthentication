from django.test import TestCase
from django.urls import reverse, resolve
from .. import views


class PasswordResetCompleteTests(TestCase):

    def setUp(self):
        url = reverse('accounts:password_reset_complete')
        self.response = self.client.get(url)

    def test_password_reset_complete_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_password_reset_complete_resolve_function(self):
        view = resolve('/accounts/reset/complete/')
        self.assertEqual(view.func.view_class, views.CustomPasswordResetCompleteView)
