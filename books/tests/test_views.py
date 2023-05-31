from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import datetime
from http import HTTPStatus

from books.models import Book, Borrower, Borrowing
class BorrowingTestCase(TestCase):
    def setUp(self):
        Book.objects.create(category=200, code=1, name='test1', author='testing', copies=5)
        Book.objects.create(category=200, code=2, name='test2', author='testing', copies=1)
        Borrower.objects.create(name='tester')
        User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')


    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('books:create-borrower'))
        self.assertRedirects(response, '/admin/login/?next=/borrow/create-borrower/')
        response = self.client.get(reverse('books:create-borrowing'))
        self.assertRedirects(response, '/admin/login/?next=/borrow/create-borrowing/')
        response = self.client.get(reverse('books:return-book'))
        self.assertRedirects(response, '/admin/login/?next=/borrow/return-book/')
        response = self.client.get(reverse('books:create-book'))
        self.assertRedirects(response, '/admin/login/?next=/books/create-book/')
        response = self.client.get(reverse('books:edit-book'))
        self.assertRedirects(response, '/admin/login/?next=/books/edit-book/')
        response = self.client.get('/books/edit-book/1/')
        self.assertRedirects(response, '/admin/login/?next=/books/edit-book/1/')
    
    def test_create_borrowing(self):
        #Logging in to get status code 200
        self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('books:create-borrowing'))
        self.assertEqual(response.status_code, HTTPStatus.OK)

        #Data for the form
        data = {
            'category': 200,
            'code': 1,
            'borrower': 1,
            'borrow_date': '2023-05-23',
        }
        response = self.client.post(reverse('books:create-borrowing'), data, follow=True)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        book1 = Book.objects.get(category=200, code=1,)
        self.assertEqual(book1.copies, 4)
        
        #Testing to borrow book test2
        data['code'] = 2
        response = self.client.post(reverse('books:create-borrowing'), data, follow=True)
        book2 = Book.objects.get(category=200, code=2,)
        self.assertFalse(book2.available)

        #Testing to borrow book test2 when out of stock to give error 406 Not Acceptable
        response = self.client.post(reverse('books:create-borrowing'), data, follow=True)
        self.assertEqual(response.status_code, HTTPStatus.NOT_ACCEPTABLE)

        #Testing bad request
        data = {
            'not_valid_field_name': 'not_valid_data'
        }
        response = self.client.post(reverse('books:create-borrowing'), data, follow=True)
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

        #Testing if book is added in borrower.books
        borrower = Borrower.objects.get(pk=1)
        book1 = Book.objects.get(pk=1)
        book1 = Book.objects.get(pk=2)
        self.assertTrue(borrower.books.contains(book1))
        self.assertTrue(borrower.books.contains(book2))
    
    def test_return_book(self):
        borrower = Borrower.objects.get(pk=1)
        book1 = Book.objects.get(pk=1)
        book2 = Book.objects.get(pk=2)
        Borrowing.objects.create(borrower=borrower, book=book1, borrow_date='2023-05-25')
        Borrowing.objects.create(borrower=borrower, book=book2, borrow_date='2023-05-25')

        #Logging in to get status code 200
        self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('books:return-book'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        #Data for the form
        data = {
            'borrowing': 1,
            'return_date': '2023-05-26',
        }

        response = self.client.post(reverse('books:return-book'), data, follow=True)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        book1 = Book.objects.get(category=200, code=1,)
        self.assertEqual(book1.copies, 5)
        #Testing return date and returned attributes
        borrowing = Borrowing.objects.get(borrower=borrower, book=book1, borrow_date='2023-05-25')
        self.assertTrue(borrowing.returned)

        data['borrowing'] = 2
        response = self.client.post(reverse('books:return-book'), data, follow=True)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        book2 = Book.objects.get(category=200, code=2,)
        self.assertTrue(book2.available)

        #Testing if book is removed from borrower.books
        borrower = Borrower.objects.get(pk=1)
        book1 = Book.objects.get(pk=1)
        book1 = Book.objects.get(pk=2)
        self.assertFalse(borrower.books.contains(book1))
        self.assertFalse(borrower.books.contains(book2))
    
    def test_edit_book(self):
        #Logging in to get status code 200
        self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('books:edit-book'))
        self.assertEqual(response.status_code, HTTPStatus.OK)

        #Data for the form
        data = {
            'category': 200,
            'code': 1,
        }
        response = self.client.post(reverse('books:edit-book'), data, follow=True)
        self.assertEqual(response.status_code, HTTPStatus.OK)

        #Testo 404 Not Found
        data['code']
        response = self.client.post(reverse('books:edit-book'), data, follow=True)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_edit_book(self):
        #Logging in to get status code 200
        self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('books:edit-book-details', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, HTTPStatus.OK)

        #Data for the form
        data = {
            'name': 'test_test1',
            'author': 'test_testing',
            'copies': 10,
        }
        #Test OK
        response = self.client.post(reverse('books:edit-book-details', kwargs={'pk': 1}), data, follow=True)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        book1 = Book.objects.get(category=200, code=1,)
        self.assertEqual(book1.name, 'test_test1')
        self.assertEqual(book1.author, 'test_testing')
        self.assertEqual(book1.copies, 10)
    
    def test_search(self):
        Book.objects.create(category=200, code=3, name='اختبار', author='testing', copies=5)
        Book.objects.create(category=200, code=4, name='test', author='أختبار', copies=5)
        #Data for the form
        data = {
            'search': 'اخت',
        }
        response = self.client.post(reverse('books:search'), data, follow=True)
        self.assertEqual(response.context['books'].count(), 1)
        self.assertEqual(response.context['books_author'].count(), 1)

