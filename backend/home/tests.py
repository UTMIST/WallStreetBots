from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status


class HomeTests(APITestCase):

    def test_home_page(self):
        url = reverse("index")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_database_connection(self):
        url = reverse("check_db")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
