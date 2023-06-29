from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from books.models import Book

class LoginTestCase(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='testuser1', password='password')
        user.is_staff = True
        user.email = 'test@mail.com'
        user.save()
        Book.objects.create(category=200, code=1, name='test', author='test')
    
    def test_redirect_if_not_logged_in(self):
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
    
    def test_status_200_if_logged_in(self):
        self.client.login(username='testuser1', password='password')
        
        response = self.client.get(reverse('books:create-borrowing'))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('books:return-book'))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('books:create-book'))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('books:edit-book'))
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/books/edit-book/1/')
        self.assertEqual(response.status_code, 200)
        
        
