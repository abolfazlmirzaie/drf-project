from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from . models import User, Product

# Create your tests here.


class ProductTestCase(APITestCase):
    def setUp(self):
        self.admin_user = User.objects.create_superuser(username='admin', password='adminpass')
        self.normal_user = User.objects.create_user(username='user', password='userpass')
        self.product = Product.objects.create(
            name="Test Product",
            description="Test Description",
            price=5.00,
            stock=5,
        )
        self.url = reverse('api:products_detail', kwargs={'pk': self.product.pk})
    def test_get_product(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unauthorized_update_product(self):
        data = {'name': 'Update Product'}
        response = self.client.put(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthorized_delete_product(self):
        response = self.client.put(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_only_admin_can_delete_product(self):

        # test normal user can not delete products
        self.client.login(username='user', password='userpass')
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Product.objects.filter(pk=self.product.pk).exists())

        # test admin user can delete product

        self.client.login(username='admin', password='adminpass')
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Product.objects.filter(pk=self.product.pk).exists())
