from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import datetime
from books.models import Book, Recommendation, Announcement, Borrowing, Subcategory
from posts.models import Post, Profile
from .serializers import AppLinkSerializer

class ZeroIndexedPagePaginationTestCase(APITestCase):
    def setUp(self):
        for i in range(20):
            Book.objects.create(name=f'book {i}', code=i, category=200)
    
    def test_page_number_page_size(self):
        #Cant test page number for now
        response = self.client.get(reverse('api:books'), {'page': 0})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 20)
        self.assertEqual(len(response.data['results']), 10)
    
class BookAPITestCase(APITestCase):
    def setUp(self):
        test_subcategory = Subcategory.objects.create(title='test_subcategory')
        
        for i in range(20):
            book = Book.objects.create(name=f'book {i}', author=f'test {i}', code=i+1, category=200)
            #Add test_subcategory to one of every 4 books
            if i % 4 == 0:
                book.subcategory.add(test_subcategory)

    def test_queryset_and_ordering(self):
        response = self.client.get(reverse('api:books'), {'page':0})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 20)
        #First book code should be 1
        self.assertEqual(response.data['results'][0]['code'], 1)
        #Last book code in page should be 10
        self.assertEqual(response.data['results'][9]['code'], 10)
    
    def test_subcategory_zero(self):
        response = self.client.get(reverse('api:books'), {'page':0, 'subcategory':0})
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 20)
    
    def test_subcategory_search(self):
        response = self.client.get(reverse('api:books'), {'page':0, 'subcategory':1})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 5)
    
    def test_filter_category(self):
        books = Book.objects.all()
        #Changing category for five books
        for book in books:
            if book.pk % 4 == 0:
                book.category = 300
                book.save()

        response = self.client.get(reverse('api:books'), {'page':0, 'category':300})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 5)   

class SubcategoryAPITestCase(APITestCase):
    def setUp(self):
        for i in range(10):
            Subcategory.objects.create(title=f'subcategory {i}')
    
    def test_subcategory_count_and_ordering(self):
        response = self.client.get(reverse('api:subcategories'), )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 10)

class PostAPITestCase(APITestCase):
    def setUp(self):
        self.profile1 = Profile.objects.create(user=User.objects.create(
            username='test_user1', password='password', first_name='test1', last_name='test1', email='gokuabdo31@gmail.com'))
        self.profile2 = Profile.objects.create(user=User.objects.create(
            username='test_user2', password='password', first_name='test2', last_name='test2', email='gokuabdo31@gmail.com'))
        for i in range(10):
            if i >= 5:
                Post.objects.create(title=f'post {1}', text=f'text {i}', approved=True, profile=self.profile2)
                continue

            Post.objects.create(title=f'post {1}', text=f'text {i}', approved=True, profile=self.profile1)
        
        for i in range(10, 20):
            Post.objects.create(title=f'post {1}', text=f'text {i}', profile=self.profile1)

    def test_queryset_only_approved_true(self):
        response = self.client.get(reverse('api:posts'), {'page':0})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 10)
    
    def test_queryset_search(self):
        response = self.client.get(reverse('api:posts'), {'page':0, 'search': 'test1'})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 5)
    
class PostCreateAPITestCase(APITestCase):
    def setUp(self):
        user = User.objects.create_user(
            username='test_user1', password='password', first_name='test1', last_name='test1', email='gokuabdo31@gmail.com')
        self.profile = Profile.objects.create(user=user)
        self.token = Token.objects.create(user=user)
        

    def test_create_post(self):
        client = APIClient()    
        client.credentials(HTTP_AUTHORIZATION='Token ' + str(self.token))
        data = {
            'profile': self.profile.id,
            'title': 'Post Title',
            'text': 'Post Text',
            'image': 'https://photo.url',
            'book': '',
        }
        response = client.post(reverse('api:create-post'), data=data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['title'], 'Post Title')
        self.assertEqual(response.data['text'], 'Post Text')
        self.assertEqual(response.data['image'], 'https://photo.url')
        self.assertIsNone(response.data['book'])

class BorrowingAPITestCase(APITestCase):
    def setUp(self):
        user = User.objects.create_user(
            username='test_user1', password='password', first_name='test1', last_name='test1', email='gokuabdo31@gmail.com')
        self.profile = Profile.objects.create(user=user)
        book = Book.objects.create(name='book', author='author', code=1, category=200, copies=10)
        self.token = Token.objects.create(user=user)
        for i in range(5):
            Borrowing.objects.create(borrower=self.profile, book=book, borrow_date=datetime.today())
        self.profile.books.add(book)
    
    def test_borrowing_queryset(self):
        client = APIClient()    
        client.credentials(HTTP_AUTHORIZATION='Token ' + str(self.token))
        response = client.get(reverse('api:borrowing'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 5)
        self.assertEqual(response.data['results'][0]['borrower_name'], self.profile.name)

class RecommendationAPITestCase(APITestCase):
    def setUp(self):
        self.book1 = Book.objects.create(name='book1', author='author', code=1, category=200, copies=10)
        self.recommendation1 = Recommendation.objects.create(title='Good Book', text='I recommend it.', book=self.book1)
        self.book2 = Book.objects.create(name='book2', author='author', code=2, category=200, copies=10)
        self.recommendation1 = Recommendation.objects.create(title='Good Book', text='I recommend it.', book=self.book2)

    def test_recommendation_query_and_ordering(self):
        response = self.client.get(reverse('api:recommendations'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['results'][0]['book'], self.book1.id)

class AnnouncementAPITestCase(APITestCase):
    def setUp(self):
        self.announcement1 = Announcement.objects.create(title='Announcement 1', text='text')
        self.announcement2 = Announcement.objects.create(title='Announcement 2', text='text')

    def test_announcement_query_and_ordering(self):
        response = self.client.get(reverse('api:announcements'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['results'][0]['id'], self.announcement1.id)
    
class GetProfleAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='test_user1', password='password', first_name='test1', last_name='test1', email='gokuabdo31@gmail.com')
        self.profile = Profile.objects.create(user=self.user)
    
    def test_get_profile_using_profile_pk(self):
        response = self.client.get(reverse('api:profile'), {'pk': self.profile.id})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['id'], self.profile.id)
        self.assertEqual(response.data['name'], 'test1 test1')
        self.assertEqual(response.data['photo'], 'https://stpeterlibrary.crabdance.com/media/')
        self.assertEqual(response.data['user'], self.user.id)
    
    def test_get_profile_using_profile_pk_not_found(self):
        response = self.client.get(reverse('api:profile'), {'pk': 5000})

        self.assertEqual(response.status_code, 404)
    
    def test_get_profile_using_user_pk(self):
        response = self.client.get(reverse('api:profile'), {'user': self.user.id})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['id'], self.profile.id)
        self.assertEqual(response.data['name'], 'test1 test1')
        self.assertEqual(response.data['photo'], 'https://stpeterlibrary.crabdance.com/media/')
        self.assertEqual(response.data['user'], self.user.id)
    
    def test_get_profile_using_user_pk_not_found(self):
        response = self.client.get(reverse('api:profile'), {'user': 5000})

        self.assertEqual(response.status_code, 404)
    
    def test_get_profile_no_query_params_not_found(self):
        response = self.client.get(reverse('api:profile'))

        self.assertEqual(response.status_code, 404)

class MyProfileAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='test_user1', password='password', first_name='test1', last_name='test1', email='gokuabdo31@gmail.com')
        self.profile = Profile.objects.create(user=self.user)
        self.token = Token.objects.create(user=self.user)
    
    def test_get_user_profile_authenticated(self):
        client = APIClient()    
        client.credentials(HTTP_AUTHORIZATION='Token ' + str(self.token))
        response = client.get(reverse('api:my-profile'))
    
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['id'], self.profile.id)
        self.assertEqual(response.data['name'], 'test1 test1')
        self.assertEqual(response.data['photo'], 'https://stpeterlibrary.crabdance.com/media/')
        self.assertEqual(response.data['user'], self.user.id)
    
    def test_get_user_profile_authenticated_not_found(self):
        self.user = User.objects.create_user(
            username='test_user2', password='password', first_name='test1', last_name='test1', email='gokuabdo31@gmail.com')
        self.token = Token.objects.create(user=self.user)

        client = APIClient()    
        client.credentials(HTTP_AUTHORIZATION='Token ' + str(self.token))
        response = client.get(reverse('api:my-profile'))

        self.assertEqual(response.status_code, 404)
    
    def test_get_user_profile_not_authenticated(self):
        response = self.client.get(reverse('api:my-profile'))

        self.assertEqual(response.status_code, 401)

class AppLinkAPITestCase(APITestCase):
    def test_get_app_link_and_version(self):
        response = self.client.get(reverse('api:app-link'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['version'], AppLinkSerializer.version)
        self.assertEqual(response.data['link'], AppLinkSerializer.link)