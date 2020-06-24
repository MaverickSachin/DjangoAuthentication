from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth.models import User
from django.core import mail


class PasswordResetMailTests(TestCase):

    def setUp(self):
        User.objects.create_user(username='admin', email='admin@gmail.com', password='personal@124')
        self.response = self.client.post(reverse('accounts:password_reset'), {'email': 'admin@gmail.com'})
        self.email = mail.outbox[0]

    def test_email_subject(self):
        self.assertEqual('[Django Tutorial] Please reset your password', self.email.subject)

    def test_email_body(self):
        context = self.response.context
        token = context.get('token')
        uid = context.get('uid')
        password_reset_token_url = reverse('accounts:password_reset_confirm', kwargs={
            'uidb64': uid,
            'token': token
        })
        self.assertIn('admin', self.email.body)
        self.assertIn('admin@gmail.com', self.email.body)

    def test_email_to(self):
        self.assertEqual(['admin@gmail.com',], self.email.to)
