from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('recent/', views.PostListView.as_view(), name='posts'),
    path('search/', views.search_posts, name='search'),
    path('<int:pk>/', views.PostDetailView.as_view(), name='details'),
    path('profile/<int:pk>/', views.posts_by_profile, name='profile-posts'),
]