from django.test import TestCase
from ..models import Post, Profile
from books.models import Book
from django.contrib.auth.models import User
from django.urls import reverse

class PostListTestCase(TestCase):
    def setUp(self):
        self.profile1 = Profile.objects.create(user=User.objects.create(
            username='test_user1', password='password', first_name='test1', last_name='test1', email='gokuabdo31@gmail.com'))
        self.profile2 = Profile.objects.create(user=User.objects.create(
            username='test_user2', password='password', first_name='test2', last_name='test2', email='gokuabdo31@gmail.com'))

        for i in range(6):
            Post.objects.create(profile=self.profile1, title=f'test_title{i}', text=f'test_text{i}',)
        for i in range(6):
            Post.objects.create(profile=self.profile2, title=f'test_title{i}', text=f'test_text{i}', approved=True)
    
    def test_post_list_view(self):
        response = self.client.get(reverse('posts:posts'))
        #Test queryset only approved=True in context (6 objects)
        self.assertEqual(response.context['posts'].count(), 6)
        #Test total count of objects is 12
        self.assertEqual(Post.objects.count(), 12)
    
    def test_post_search_by_title_text(self):
        response = self.client.post(reverse('posts:search'), {'search': 'test_title'})
        self.assertEqual(response.context['posts'].count(), 6)
        
        response = self.client.post(reverse('posts:search'), {'search': 'test_text'})
        self.assertEqual(response.context['posts'].count(), 6)

    def test_post_search_by_profile_name(self):
        response = self.client.post(reverse('posts:search'), {'search': 'test2 test2'})
        self.assertEqual(response.context['posts'].count(), 6)
        
        response = self.client.post(reverse('posts:search'), {'search': 'test2'})
        self.assertEqual(response.context['posts'].count(), 6)
        
        response = self.client.post(reverse('posts:search'), {'search': 'test1 test1'})
        self.assertEqual(response.context['posts'].count(), 0)
    
    def test_search_posts_by_profile(self):
        response = self.client.post(reverse('posts:profile-posts', kwargs={'pk': 1}))
        self.assertEqual(response.context['posts'].count(), 0)

        response = self.client.post(reverse('posts:profile-posts', kwargs={'pk': 2}))
        self.assertEqual(response.context['posts'].count(), 6)
    
class PostCreateTestCase(TestCase):
    def setUp(self):
        self.profile1 = Profile.objects.create(user=User.objects.create_user(
            username='test_user1', password='1X<ISRUkw+tuK', first_name='test1', last_name='test1', email='gokuabdo31@gmail.com'))
        
        Book.objects.create(category=200, code=1, name='book', author='author')
     
    def test_create_post_no_book_no_image(self):
        self.client.login(username='test_user1', password='1X<ISRUkw+tuK')

        data = {
            'title': 'This is a test post title.',
            'text': 'This is a test post text.',
            'book': '',
            'image': '',
        }
        response = self.client.post(reverse('posts:create-post'), data, follow=True)
        
        post = Post.objects.get(pk=1) 
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context.get('success', False))
        self.assertEqual(post.title, 'This is a test post title.')
        self.assertEqual(post.text, 'This is a test post text.')
        self.assertIsNone(post.book)
        self.assertEqual(post.image, '')
    
    def test_create_post_book_and_image_provided(self):
        self.client.login(username='test_user1', password='1X<ISRUkw+tuK')
        
        data = {
            'title': 'This is a test post title.',
            'text': 'This is a test post text.',
            'book': 1,
            'image': 'https://tpc.googlesyndication.com/simgad/2894417314404102158',
        }    
        response = self.client.post(reverse('posts:create-post'), data, follow=True)

        post = Post.objects.get(pk=1)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context.get('success', False))
        self.assertEqual(post.book, Book.objects.get(pk=1))
        self.assertEqual(post.image, 'https://tpc.googlesyndication.com/simgad/2894417314404102158')
    
    def test_create_post_error(self):
        self.client.login(username='test_user1', password='1X<ISRUkw+tuK')
        
        data = {
            'Not a valid field name': 'Not valid data'
        }    
        response = self.client.post(reverse('posts:create-post'), data, follow=True)

        self.assertEqual(response.status_code, 406)
        self.assertTrue(response.context.get('error', False))