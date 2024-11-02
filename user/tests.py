from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User

class UserAuthTests(APITestCase):

    def setUp(self):
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.logout_url = reverse('logout')
        self.user_data = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        # Create a user for testing login/logout
        self.user = User.objects.create_user(**self.user_data)

    # Test the registration functionality
    def test_user_can_register(self):
        response = self.client.post(self.register_url, {
            'username': 'newuser',
            'password': 'newpassword'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_registration_when_authenticated(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(self.register_url, {
            'username': 'anotheruser',
            'password': 'anotherpassword'
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # Test the login functionality
    def test_user_can_login(self):
        response = self.client.post(self.login_url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_with_invalid_credentials(self):
        response = self.client.post(self.login_url, {
            'username': 'wronguser',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # Test the logout functionality
    def test_user_can_logout(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(self.logout_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logout_without_authentication(self):
        response = self.client.get(self.logout_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # Test that the model can be saved to the database
    def test_user_model_can_be_saved(self):
        user = User.objects.create_user(username='saveduser', password='savedpassword')
        self.assertTrue(User.objects.filter(username='saveduser').exists())

    # Test that the model can be retrieved from the database
    def test_user_model_can_be_retrieved(self):
        user = User.objects.get(username='testuser')
        self.assertEqual(user.username, 'testuser')

    # Test that the model can be updated in the database
    def test_user_model_can_be_updated(self):
        user = User.objects.get(username='testuser')
        user.username = 'updateduser'
        user.save()
        self.assertEqual(User.objects.get(id=user.id).username, 'updateduser')

