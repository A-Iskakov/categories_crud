"""applications tests for views.py check"""

from django.contrib.auth.models import User
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APIClient


class UserTests(APITestCase):
    """user CRUD functionality check"""
    def setUp(self):
        """create test data"""
        User.objects.create_user(**{
            "first_name": "string",
            "last_name": "string",
            "email": "user@example.com",
            "username": "stri12ng",
            "password": "stri123ng"
        })

    def test_register(self):
        """test register user process"""
        c = APIClient()
        response = c.post(reverse('user-accounts-register'),
                          {
                              "first_name": "string",
                              "last_name": "string",
                              "email": "user@example.com",
                              "username": "stri123ng",
                              "password": "stri123ng"
                          }
                          )
        # print(User.objects.all())
        self.assertEqual(response.json()['Status'], True)

    def test_login_logout(self):
        """check login and logout procedure"""
        c = APIClient()
        response = c.post(reverse('user-accounts-login'),
                          {
                              "username": "stri12ng",
                              "password": "stri123ng"
                          }
                          ).json()

        self.assertEqual(response['Status'], True)
        token = response['Data']['Authorization']
        # print(token)
        c.credentials(HTTP_AUTHORIZATION=token)
        response = c.get(reverse('user-accounts-logout')).json()
        self.assertEqual(response['Status'], True)
