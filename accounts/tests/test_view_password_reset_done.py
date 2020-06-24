from django.test import TestCase
from django.urls import reverse, resolve
from .. import views


class PasswordResetDoneTests(TestCase):

    def setUp(self):
        url = reverse('accounts:password_reset_done')
        self.response = self.client.get(url)

    def test_password_reset_done_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_password_reset_done_view_function(self):
        view = resolve('/accounts/reset/done/')
        self.assertEqual(view.func.view_class, views.CustomPasswordResetDoneView)
