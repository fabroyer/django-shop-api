from django.urls import reverse_lazy, reverse
from rest_framework.test import APITestCase

from shop.models import Category


class ShopAPITestCase(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.category = Category.objects.create(name='Fruits', active=True)
        Category.objects.create(name='Légumes', active=False)

        cls.category_2 = Category.objects.create(name='Légumes', active=True)

    def format_datetime(self, value):
        return value.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

class TestCategory(ShopAPITestCase):

    url = reverse_lazy('category-list')

    def test_list(self):
        category = Category.objects.create(name='Fruits', active=True)
        Category.objects.create(name='Légumes', active=False)

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

        expected = [
            {
                'id': category.id,
                'name': category.name,
                'date_created': self.format_datetime(category.date_created),
                'date_updated': self.format_datetime(category.date_updated)
            } for category in [self.category, self.category_2]
        ]
        self.assertEqual(response.json(), expected)

    def test_create(self):
        category_count = Category.objects.counts()
        response = self.client.post(self.url, data={'name': 'Tentative'})
        self.assertEqual(response.status_code, 405)
        self.assertFalse(Category.objects.count(), category_count)
