from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from users.models import User


class UserCRUDTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            'email': 'testuser@example.com',
            'password': 'testpassword',
            'first_name': 'Test',
            'last_name': 'User',
            'telephone': '1234567890',
            'image': None,
            'country': 'Country',
            'city': 'City',
        }
        self.user = User.objects.create(**self.user_data)
        self.url_create = reverse('users:users-create')
        self.url_retrieve = reverse('users:user-retrieve', args=[self.user.pk])
        self.url_update = reverse('users:users-update', args=[self.user.pk])
        self.url_destroy = reverse('users:users-destroy', args=[self.user.pk])

    def test_create_user(self):
        self.client.force_authenticate(user=self.user)
        new_user_data = {
            'email': 'newuser@example.com',
            'password': 'newuserpassword',
            'password2': 'newuserpassword',
            'first_name': 'New',
            'last_name': 'User',
            'telephone': '9876543210',
        }
        response = self.client.post(
            self.url_create,
            new_user_data
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)

    def test_retrieve_user_profile(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url_retrieve)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], self.user.email)

    def test_update_user_profile(self):
        self.client.force_authenticate(user=self.user)
        updated_data = {
            'first_name': 'Updated',
            'last_name': 'User',
            'telephone': '9876543210',
        }
        response = self.client.put(
            self.url_update,
            updated_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Updated')
        self.assertEqual(self.user.telephone, '9876543210')

    def test_delete_user_profile(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.url_destroy)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(User.objects.count(), 0)
