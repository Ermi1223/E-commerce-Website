from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
from products.models import Product

class UserTests(APITestCase):

    def test_register_user(self):
        url = reverse('register')
        data = {'username': 'testuser', 'password': 'testpassword'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_login_user(self):
        user = User.objects.create_user(username='testuser', password='testpassword')
        url = reverse('login')
        data = {'username': 'testuser', 'password': 'testpassword'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    

    # More tests for products, CRUD operations, etc.


class ProductTests(APITestCase):

    def setUp(self):
        # Create a test user for authorized tests
        self.user = User.objects.create_user(username='testuser', password='testpassword')
    
    def test_create_product_unauthorized(self):
        # Test that an unauthorized user cannot create a product
        url = reverse('create_product')  # Ensure this matches your URL name
        data = {'name': 'Test Product', 'description': 'A test product', 'price': 99.99}
        
        # Do not authenticate, so it should fail with 401 Unauthorized
        response = self.client.post(url, data, format='json')
        
        # Assert that the status code is 401 Unauthorized
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
 
    

    