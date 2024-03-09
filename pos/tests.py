from django.test import TestCase
from django.urls import reverse
from .models import Customer, Product
from django.contrib.auth.models import User


class CustomerDeleteViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a test customer
        cls.customer = Customer.objects.create(identity=1, name='Test Customer', balance=100.00)

    def test_customer_delete_view(self):
        # Get the URL of the customer delete view for the test customer
        url = reverse('customer_delete', kwargs={'pk': self.customer.identity})

        # Send a POST request to delete the customer
        response = self.client.post(url)

        # Check that the response status code is 302 (redirect)
        self.assertEqual(response.status_code, 302)

        # Check that the customer has been deleted
        self.assertFalse(Customer.objects.filter(identity=self.customer.identity).exists())


class ProductDetailViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a test user
        cls.user = User.objects.create_user(username='testuser', password='12345')

        # Create a test product
        cls.product = Product.objects.create(name='Test Product', price=10.00)

    def test_product_detail_view(self):
        # Log in as the test user
        self.client.login(username='testuser', password='12345')

        # Get the URL of the product detail view for the test product
        url = reverse('product_detail', kwargs={'pk': self.product.pk})

        # Send a GET request to the product detail view
        response = self.client.get(url)

        # Check that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Check that the correct template is used
        self.assertTemplateUsed(response, 'pos/product_details.html')

        # Check that the product is present in the context
        self.assertIn('object', response.context)

        # Check that the product in the context is the test product
        product_in_context = response.context['object']
        self.assertEqual(product_in_context, self.product)

    def test_product_detail_view_permissions(self):
        # Create a new user (not the owner of the product)
        other_user = User.objects.create_user(username='otheruser', password='54321')

        # Log in as the new user
        self.client.login(username='otheruser', password='54321')

        # Get the URL of the product detail view for the test product
        url = reverse('product_detail', kwargs={'pk': self.product.pk})

        # Send a GET request to the product detail view
        response = self.client.get(url)

        # Check that the response status code is 403 (Forbidden)
        self.assertEqual(response.status_code, 403)
