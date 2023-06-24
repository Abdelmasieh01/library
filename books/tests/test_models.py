from django.test import TestCase
from ..models import Book, Borrowing, Recommendation, Announcement
from posts.models import Profile
from datetime import datetime
from django.contrib.auth.models import User


class BookTestCase(TestCase):
    def setUp(self):
        Book.objects.create(category=200, age_category=1,
                            code=1, name='test', author='test_author', copies=1)

    def test_str(self):
        book = Book.objects.get(category=200, code=1)
        self.assertEqual(book.__str__(), f'test - 200 - 1 - test_author')


class BorrowingTestCase(TestCase):
    def setUp(self):
        book = Book.objects.create(category=200, age_category=1,
                            code=1, name='test', author='test_author', copies=1)
        self.profile = Profile.objects.create(user=User.objects.create(
            username='test_user', password='test', first_name='test', last_name='test'), )
        self.borrowing = Borrowing.objects.create(borrower=self.profile, book=book, borrow_date=datetime.today())

    def test_borrowing_str(self):
        self.assertEqual(self.borrowing.__str__(), 'test test: test')
    
    def test_save_book_count_and_book_available_returned_false(self):
        book = Book.objects.get(pk=1)
        book.copies -= 1
        book.available = False
        book.save()
        
        self.assertEqual(book.copies, 0)
        self.assertFalse(book.available)
    
    def test_save_book_count_and_book_available_returned_true(self):
        self.borrowing.returned = True
        self.borrowing.return_date = datetime.today()
        self.borrowing.save()

        book = Book.objects.get(pk=1)

        self.assertEqual(book.copies, 1)
        self.assertTrue(book.available)
    
    def test_str(self):
        self.assertEqual(self.borrowing.__str__(), 'test test: test')

class RecommendationTestCase(TestCase):
    def setUp(self):
        book = Book.objects.create(category=200, age_category=1,
                            code=1, name='test', author='test_author', copies=1)
        self.recommendation = Recommendation.objects.create(book=book, title='test', text='test')

    def test_recommendation_str(self):
        self.assertEqual(self.recommendation.__str__(), 'ترشيح لكتاب: test')

class AnnouncementTestCase(TestCase):
    def setUp(self):
        self.announcement = Announcement.objects.create(title='test title', text='test text')
    
    def test_str(self):
        self.assertEqual(self.announcement.__str__(), 'test title')