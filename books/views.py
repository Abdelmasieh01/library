from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.db.models import Q
from django.views.generic import CreateView
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
from http import HTTPStatus
from .models import Book, Borrowing, Recommendation, Subcategory, Announcement
from .forms import BorrowingForm, ReturnForm, BookForm, BookUpdateForm
from posts.models import Post, Profile
from datetime import datetime, timedelta


def index(request):
    categories = ((0, 'الكل'),) + Book.CATEGORIES
    subcategories = Subcategory.objects.all()
    unapproved_posts = Post.objects.filter(approved=False)
    late_borrowings = Borrowing.objects.filter(returned=False).filter(
        borrow_date__lte=datetime.now().date() - timedelta(days=15))
    recommendations = Recommendation.objects.order_by('-timestamp').prefetch_related()[:3]
    announcements = Announcement.objects.filter(show=True)[:5]
    return render(request, 'books/index.html', {'categories': categories, 'subcategories': subcategories, 'announcements':announcements, 'recommendations': recommendations, 'posts_count': unapproved_posts.count(), 'late_count': late_borrowings.count()})


def search(request):
    categories = ((0, 'الكل'),) + Book.CATEGORIES
    subcategories = Subcategory.objects.all()
    
    if request.method == 'POST':
        keyword = request.POST.get('search', '')
        category = request.POST.get('category', None)
        subcategory = request.POST.get('subcategory', None)

        books = books_author = Book.objects.all()
        books_author = None

        if category and (category != '0'):
            books = books.filter(category=int(category))

        if subcategory and (subcategory != '0'):
            books = books.filter(subcategory=int(subcategory))

        if keyword != '' and keyword != ' ': 
            keyword_var1 = keyword.replace('ا', 'أ')
            keyword_var2 = keyword.replace('ي', 'ى')
            keyword_var3 = keyword_var2.replace('ا', 'أ')
            books = books.filter(Q(name__icontains=keyword) | Q(name__icontains=keyword_var1) | Q(
                name__icontains=keyword_var2) | Q(name__icontains=keyword_var3) | Q(author__icontains=keyword) | Q(author__icontains=keyword_var1) | Q(
                author__icontains=keyword_var1) | Q(author__icontains=keyword_var1)).order_by('category', 'code')

    else:
        books = Book.objects.all().order_by('?')[:50]
        books_author = None
        keyword = ''

    context = {'books': books, 'books_author': books_author, 'keyword': keyword, 'categories': categories, 'subcategories': subcategories}
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


def try_borrow(book: Book, borrower: Profile, date) -> bool:
    if book.copies > 0:
        borrowing = Borrowing(borrower=borrower, borrow_date=date, book=book)
        book.copies -= 1
        book.available = borrowing.book.copies > 0
        borrower.books.add(borrowing.book)
        book.save()
        borrowing.save()
        return True
    else:
        return False


@login_required(login_url='/admin/login/')
@staff_member_required
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

            success = try_borrow(book, borrower, date)
            if not success:
                return render(request, 'books/borrowing_form.html', {'form': form, 'error': True}, status=HTTPStatus.NOT_ACCEPTABLE)

            return redirect('books:create-borrowing')
        else:
            form = BorrowingForm()
            return render(request, 'books/borrowing_form.html', {'form': form, 'error': True}, status=HTTPStatus.BAD_REQUEST)

    form = BorrowingForm()
    return render(request, 'books/borrowing_form.html', {'form': form})


@login_required(login_url='/admin/login/')
@staff_member_required
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


@method_decorator(staff_member_required, name='dispatch')
class BookCreateView(LoginRequiredMixin, CreateView):
    login_url = '/admin/login/'
    model = Book
    form_class = BookForm
    template_name = 'books/book_form.html'

    def get_success_url(self):
        return reverse('books:create-book',)


@login_required(login_url='/admin/login/')
@staff_member_required
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
@staff_member_required
def edit_book_details(request, pk=2653):
    if request.method == 'POST':
        form = BookUpdateForm(request.POST)
        if form.is_valid():
            try:
                book = Book.objects.get(pk=pk)
                book.name = form.cleaned_data['name']
                book.author = form.cleaned_data['author']
                book.copies = form.cleaned_data['copies']
                book.image = form.cleaned_data['image']
                book.link = form.cleaned_data['link']
                # book.subcategory.add(form.cleaned_data['subcategory'])
                book.available = book.copies > 0
                book.save()
                return redirect('books:edit-book-details', pk=book.pk)
            except:
                return render(request, 'books/book_edit.html', {'form': form, 'error': True}, status=HTTPStatus.NOT_FOUND)

    book = Book.objects.get(pk=pk)
    form = BookUpdateForm(instance=book)
    return render(request, 'books/book_edit.html', {'form': form, 'error': False})

@csrf_exempt
def send_email_to_instatech(request):
    if request.method == 'POST':
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        message = request.POST.get('message', '')
        try:
            send_mail(
                subject=f'Email From: {name}',
                message=f'''
                Name: {name}
                Email: {email}
                Phone: {phone}
                Message: {message}
                ''',
                from_email= 'instaTech Email <stpeterlibrary39@gmail.com>',
                recipient_list=['instatech36@gmail.com']
            )
            return redirect('https://instatech36.github.io/success/')
        except:
            return redirect('https://instatech36.github.io/error/')
    else:
        return redirect('https://instatech36.github.io/')