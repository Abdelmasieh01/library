from django.test import TestCase
from django.contrib.auth.models import User
from django.core import mail
from django.contrib import messages
from django.contrib.messages.storage.fallback import FallbackStorage
from django.contrib.admin.sites import AdminSite
from datetime import datetime
from ..models import Book, Borrowing
from ..admin import send_late_return_email, BorrowingAdmin
from posts.models import Profile

class LateBorrowingEmailTestCase(TestCase):
    def setUp(self):
        self.site = AdminSite()
        self.model_admin = BorrowingAdmin(Borrowing, self.site)
        self.book = Book.objects.create(category=200, code=1, name='test', author='test', copies=5)

    def test_send_late_return_email(self):
        #user 1, superuser to access admin panel and with email
        user = User.objects.create_user(username='test1', password='password')
        user.is_staff = user.is_superuser = True
        user.email = 'gokuabdo31@gmail.com'
        user.save()
        profile = Profile.objects.create(user=user)
        borrowing = Borrowing.objects.create(book=self.book, borrower=profile, borrow_date=datetime.today())
        queryset = [borrowing]

        self.client.login(username='test1', password='password')
        request = self.client.request().wsgi_request
        
        send_late_return_email(self.model_admin, request, queryset)

        self.assertEqual(len(mail.outbox), 1)
        sent_email = mail.outbox[0]
        self.assertEqual(sent_email.subject, 'لقد تأخرت في إرجاع كتاب للمكتبة!')
        self.assertEqual(sent_email.body, f'لقد تأخرت في إرجاع كتاب {borrowing.book.name}')
        self.assertEqual(sent_email.from_email, 'St. Peter Library <stpeterlibrary39@gmail.com>')
        self.assertEqual(sent_email.to, [user.email])

    def test_send_late_return_email_error_no_email(self):
        user = User.objects.create_user(username='test1', password='password')
        user.is_staff = user.is_superuser = True
        user.save()
        profile = Profile.objects.create(user=user)
        borrowing = Borrowing.objects.create(book=self.book, borrower=profile, borrow_date=datetime.today())
        queryset = [borrowing]

        self.client.login(username='test1', password='password')
        request = self.client.request().wsgi_request
        setattr(request, '_messages', FallbackStorage(request))
        messages.set_level(request, messages.ERROR)
        
        send_late_return_email(self.model_admin, request, queryset)

        messages_list = list(messages.get_messages(request))
        self.assertEqual(len(messages_list), 1)
        message = messages_list[0]
        self.assertEqual(message.level, messages.ERROR)
        self.assertEqual(str(message), f'البريد الإلكتروني ل{borrowing.borrower.name} غير مسجل')
