from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.views.generic import CreateView
from http import HTTPStatus
from .models import Book, Borrowing
from .forms import BorrowingForm, ReturnForm, BookForm, BookUpdateForm


def index(request):
    categories = Book.CATEGORIES
    return render(request, 'books/index.html', {'categories': categories})


def search(request):
    keyword = request.POST.get('search', '')
    keyword_var1 = keyword.replace('ا', 'أ')
    keyword_var2 = keyword.replace('ي', 'ى')
    keyword_var3 = keyword_var2.replace('ا', 'أ')
    books = Book.objects.filter(Q(name__icontains=keyword) | Q(name__icontains=keyword_var1) | Q(
        name__icontains=keyword_var2) | Q(name__icontains=keyword_var3)).order_by('category', 'code')
    books_author = Book.objects.filter(Q(author__icontains=keyword) | Q(author__icontains=keyword_var1) | Q(
        author__icontains=keyword_var1) | Q(author__icontains=keyword_var1)).order_by('category', 'code')
    context = {'books': books,
               'books_author': books_author, 'keyword': keyword}
    return render(request, 'books/search.html', context)

'''
class BorrowerCreateView(LoginRequiredMixin, CreateView):
    login_url = '/admin/login/'
    model = Borrower
    form_class = BorrowerForm
    template_name = 'books/borrower_form.html'

    def get_success_url(self):
        return reverse('books:create-borrower',)
'''


@login_required(login_url='/admin/login/')
def create_borrowing(request):
    if request.method == 'POST':
        form = BorrowingForm(request.POST)
        if form.is_valid():
            category = form.cleaned_data['category']
            code = form.cleaned_data['code']

            try:
                book = Book.objects.get(category=category, code=code)
            except:
                return render(request, 'books/borrowing_form.html', {'form': form, 'error': True})

            borrower = form.cleaned_data['borrower']
            date = form.cleaned_data['borrow_date']
            if book.copies > 0:
                borrowing = Borrowing(borrower=borrower, borrow_date=date, book=book)
                book.copies -=1
                book.available = borrowing.book.copies > 0
                borrower.books.add(borrowing.book)
                book.save() 
                borrowing.save()
            else:
                return render(request, 'books/borrowing_form.html', {'form': form, 'error': True}, status=HTTPStatus.NOT_ACCEPTABLE)
            
            return redirect('books:create-borrowing')
        else:
            form = BorrowingForm()
            return render(request, 'books/borrowing_form.html', {'form': form, 'error': True}, status=HTTPStatus.BAD_REQUEST)
    
    form = BorrowingForm()
    return render(request, 'books/borrowing_form.html', {'form': form})


@login_required(login_url='/admin/login/')
def return_book(request):
    if request.method == 'POST':
        form = ReturnForm(request.POST)
        if form.is_valid():
            borrowing = form.cleaned_data['borrowing']
            borrowing.return_date = form.cleaned_data['return_date']
            borrowing.returned = True
            borrowing.book.copies += 1
            borrowing.book.available = True
            borrowing.borrower.books.remove(borrowing.book)
            borrowing.book.save()
            borrowing.save()
            return redirect('books:return-book')
        else: 
            return render(request, 'books/return_book.html', {'form': form, 'error': True}, status=HTTPStatus.NOT_ACCEPTABLE)
            
    form = ReturnForm()
    return render(request, 'books/return_book.html', {'form': form})


class BookCreateView(LoginRequiredMixin, CreateView):
    login_url = '/admin/login/'
    model = Book
    form_class = BookForm
    template_name = 'books/book_form.html'

    def get_success_url(self):
        return reverse('books:create-book',)


@login_required(login_url='/admin/login/')
def edit_book(request):
    if request.method == 'POST':
        try:
            category = request.POST.get('category', '')
            code = request.POST.get('code', '')
            book = Book.objects.get(category=category, code=code)
            return redirect('books:edit-book-details', book.pk)
        except:
            form = False
            error = True
            return render(request, 'books/book_edit.html', {'form': form, 'error': error}, status=HTTPStatus.NOT_FOUND)

    form = False
    error = False
    return render(request, 'books/book_edit.html', {'form': form, 'error': error})


@login_required(login_url='/admin/login/')
def edit_book_details(request, pk=2653):
    if request.method == 'POST':
        form = BookUpdateForm(request.POST)
        if form.is_valid():
            try:
                book = Book.objects.get(pk=pk)
                book.name = form.cleaned_data['name']
                book.author = form.cleaned_data['author']
                book.copies = form.cleaned_data['copies']
                book.available = book.copies > 0
                book.save()
                return redirect('books:edit-book-details', pk=book.pk)
            except:
                error = True
                return render(request, 'books/book_edit.html', {'form': form, 'error': error}, status=HTTPStatus.NOT_FOUND)

    book = Book.objects.get(pk=pk)
    form = BookUpdateForm(instance=book)
    error = False
    return render(request, 'books/book_edit.html', {'form': form, 'error': error})
