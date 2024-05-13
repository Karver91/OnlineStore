from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse

from users.models import User, EmailConfirmation


class UserRegistrationViewTestCase(TestCase):
    def setUp(self):
        self.data = {
            'first_name': 'Ivan', 'last_name': 'Ivanov', 'username': 'Ivan', 'email': 'ivanov@gmail.com',
            'password1': 'qwertadfgh', 'password2': 'qwertadfgh'
        }
        self.path = reverse('OnlineStore_users:registration')

    def test_user_registration_get(self):
        response = self.client.get(self.path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'users/registration.html')

    def test_user_registration_post(self):
        username = self.data['username']
        self.assertFalse(User.objects.filter(username=username).exists())
        response = self.client.post(self.path, self.data)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTrue(User.objects.filter(username=username).exists())

        email_confirmation = EmailConfirmation.objects.filter(user__username=username)
        self.assertTrue(email_confirmation.exists())
