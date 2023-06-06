from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [
    path('books/', views.BookListAPIView.as_view(), name='books'),
    path('posts/', views.PostAPIView.as_view(), name='posts'),
    path('book/', views.get_book, name='book'),
    path('post/', views.get_post, name='post'),
    path('profile/', views.get_profile, name='profile'),
    path('my-profile/', views.my_profile, name='my-profile')
]