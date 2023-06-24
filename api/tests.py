from rest_framework.test import APITestCase
from rest_framework.test import APIClient as client
from django.urls import reverse
from books.models import Book

class ZeroIndexedPagePaginationTestCase(APITestCase):
    def setUp(self):
        for i in range(20):
            Book.objects.create(name=f'book {i}', code=i, category=200)
    
    def TestPageNumber(self):
        pass