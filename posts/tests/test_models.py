from django.test import TestCase
from ..models import Profile, Post
from books.models import Book
from django.contrib.auth.models import User


class ProfileTestCase(TestCase):
    def setUp(self):
        self.profile = Profile.objects.create(user=User.objects.create_user(
            username='test', password='password', first_name='test1', last_name='test2', email='gokuabdo31@gmail.com'))
        self.book = Book.objects.create(category=200, code=1, name='test', author='test')

    def test_profile_str_name(self):
        self.assertEqual(self.profile.__str__(), 'test1 test2')
        self.assertEqual(self.profile.name(), 'test1 test2')
    
    def test_count_books(self):
        self.profile.books.add(self.book)
        self.assertEqual(self.profile.count_books(), 1)

class PostTestCase(TestCase):
    def setUp(self):
        self.profile = Profile.objects.create(user=User.objects.create_user(
            username='test', password='password', first_name='test1', last_name='test2', email='gokuabdo31@gmail.com'))
        self.book = Book.objects.create(category=200, code=1, name='test', author='test')
        self.post1 = Post.objects.create(profile=self.profile, book=self.book, title='title', text='text', approved=True)

    def test_post_str_(self):
        self.assertEqual(self.post1.__str__(), 'title للكاتب: test1 test2')
