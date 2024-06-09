from django.urls import reverse
from django.test import TestCase, RequestFactory
from rest_framework.test import force_authenticate, APIClient
from core.models import User, Product, Order, OrderItem
from product.views import ProductViewSet
import json

class ProductTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create(email='test@example.com', name='Test User', is_staff=True)
        self.product = Product.objects.create(name='Test Product',
                                              price=1000, quantity=10, description='Test Description', size='M', user=self.user, category='Shorts',
                                              )
        self.client = APIClient()

    def test_create_order(self):
        self.client.force_authenticate(user=self.user)
        url = url = '/api/v1/orders/create_orders/'
        data = {
            'street_address': '123 Test St',
            'city': 'Test City',
            'zip_code': '12345',
            'country': 'Test Country',
            'order_items': [
                {
                    'product_id': self.product.id,
                    'quantity': 2,
                    'price': 10
                }
            ]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(OrderItem.objects.count(), 1)
        self.product.refresh_from_db()
        self.assertEqual(self.product.quantity, 98)
    
    def test_create_order_empty_items(self):
        self.client.force_authenticate(user=self.user)
        url = url = '/api/v1/orders/create_orders/'
        data = {
            'street_address': '123 Test St',
            'city': 'Test City',
            'zip_code': '12345',
            'country': 'Test Country',
            'order_items': []
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('Order items cannot be empty', response.data['error'])
    
    def test_create_order_unauthenticated(self):
        url = url = '/api/v1/orders/create_orders/'
        data = {
            'street_address': '123 Test St',
            'city': 'Test City',
            'zip_code': '12345',
            'country': 'Test Country',
            'order_items': [
                {
                    'product_id': self.product.id,
                    'quantity': 2,
                    'price': 10
                }
            ]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 401)