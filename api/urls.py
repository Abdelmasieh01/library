from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [
    path('books/', views.BookListAPIView.as_view(), name='books'),
    path('posts/', views.PostAPIView.as_view(), name='posts'),
    path('profile/', views.get_profile, name='profile'),
    path('my-profile/', views.my_profile, name='my-profile'),
    path('create-post/', views.PostCreateAPIView.as_view(), name='create-post'),
    path('borrowing/', views.BorrowingAPIView.as_view(), name='borrowing'),
    path('recommendations/', views.RecommendationAPIView.as_view(), name='recommendations'),
    path('announcements/', views.AnnouncementAPIView.as_view(), name='announcements'),
    path('app-link/', views.app_link, name='app-link'),
    path('subcategories/', views.SubcategoryAPIView.as_view(), name='subcategories')
]