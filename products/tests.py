from http import HTTPStatus

from django.core.paginator import Paginator
from django.db.models import Count
from django.test import TestCase
from django.urls import reverse

from products.models import Category, Product


class IndexViewTestCase(TestCase):
    def test_view(self):
        path = reverse('home')
        response = self.client.get(path)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'products/index.html')


class CatalogViewTestCase(TestCase):
    fixtures = ['fixtures.json']

    def setUp(self):
        path = reverse('OnlineStore_products:catalog')
        self.response = self.client.get(path)

    def test_view(self):
        self.assertEqual(self.response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(self.response, 'products/catalog.html')

    def test_list_with_category(self):
        categories = Category.objects.all()
        self.assertQuerysetEqual(self.response.context_data.get('categories'), categories, ordered=False)

    def test_list_with_products(self):
        db_objects = Product.objects.filter(inventory__quantity__gt=0).annotate(
                num_products=Count('id')).order_by('id')

        paginator = Paginator(db_objects, 3)  # Пагинируем объекты
        page_number = 1
        while page_number <= paginator.num_pages:
            html_objects = self.response.context['object_list']  # Получаем объекты, отображаемые на странице
            expected_objects = paginator.page(page_number).object_list  # Получаем объекты для текущей страницы
            self.assertQuerysetEqual(html_objects, expected_objects, ordered=False)  # Сравниваем объекты
            page_number += 1
            if page_number <= paginator.num_pages:
                self.response = self.client.get(reverse('OnlineStore_products:catalog') + f'?page={page_number}')

