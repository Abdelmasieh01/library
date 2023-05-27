from django.test import TestCase
from ..models import Book, Borrower, Borrowing

# Create your tests here.
class BorrowerTestCase(TestCase):
    def setUp(self):
        Book.objects.create(category=200, code=1, name='test1', author='testing', copies=5)
        Book.objects.create(category=200, code=2, name='test2', author='testing', copies=1)
        Borrower.objects.create(name='tester')
    
    def test_borrower_count(self):
        borrower = Borrower.objects.get(name='tester')
        book1 = Book.objects.get(category=200, code=1)
        book2 = Book.objects.get(category=200, code=2)
        borrower.books.add(book1)
        borrower.books.add(book2)
        self.assertEqual(borrower.count_books(), 2)
        