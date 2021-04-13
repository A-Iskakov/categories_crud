from django.contrib.auth.models import User
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APIRequestFactory, APIClient


class UserTests(APITestCase):

    def test_register(self):
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

    def test_login(self):
        c = APIClient()
        response = c.post(reverse('user-accounts-login'),
                          {
                              "username": "stri123ng",
                              "password": "stri123ng"
                          }
                          )
        print(User.objects.all())
        print(response.json())
        self.assertEqual(response.json()['Status'], True)