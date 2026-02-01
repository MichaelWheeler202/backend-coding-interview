from django.test import TestCase, Client
from django.contrib.auth.models import User
from rest_framework import status


class AuthorizationTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )


    def test_non_logged_in_account_401s_on_secure_endpoint(self):
        response = self.client.get('/photo_api/photos/1/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual("You must be signed in with github SSO to access this endpoint.", response.content.decode())

    def test_non_logged_in_account_accesses_login_endpoint(self):
        response = self.client.get('/admin/login')
        self.assertNotEqual(response.status_code, status.HTTP_200_OK)

    def test_logged_in_account_accesses_secure_endpoint(self):
        try:
            self.client.login(username='testuser', password='testpass123')
            response = self.client.get('/photo_api/photos/1/')
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
            responseData = response.json()
            self.assertEqual("Photo ID 1 does not exist.", responseData["error"])
        finally:
            self.client.logout()


