from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [
    path('books/', views.BookAPIView.as_view(), name='books'),
    path('posts/', views.PostAPIView.as_view(), name='posts'),
    path('profile/', views.get_profile, name='profile'),
]