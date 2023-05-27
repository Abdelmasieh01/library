from django.urls import path
from . import views

app_name = 'books'

urlpatterns = [
    path('', views.index, name='index'),
    path('search/', views.search, name='search'),
    path('borrow/create-borrower/', views.BorrowerCreateView.as_view(), name='create-borrower'),
    path('borrow/create-borrowing/', views.create_borrowing, name='create-borrowing'),
    path('borrow/return-book/', views.return_book, name='return-book'),
    path('books/create-book/', views.BookCreateView.as_view(), name='create-book'),
    path('books/edit-book/', views.edit_book, name='edit-book'),
    path('books/edit-book/<int:pk>/', views.edit_book_details, name='edit-book-details'),
]