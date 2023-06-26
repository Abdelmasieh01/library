from django.db import models
from django.contrib.auth.models import User

from books.models import Book

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='الحساب')
    photo = models.ImageField(blank=True, null=True, upload_to='profile_photos', verbose_name='الصورة')
    books = models.ManyToManyField(Book, blank=True, verbose_name='الكتب التي استعارها')

    def __str__(self):
        return self.name
    
    @property
    def name(self):
        return self.user.first_name + ' ' + self.user.last_name

    @property
    def count_books(self):
        return self.books.count() 

class Post(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name='الكاتب')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, null=True, blank=True, verbose_name='الكتاب')
    title = models.CharField(max_length=255, verbose_name='العنوان')
    text = models.TextField(max_length=50000, verbose_name='النص')
    image = models.URLField(blank=True, verbose_name='الصورة')
    approved = models.BooleanField(default=False, verbose_name='قبول المشاركة')
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name='التاريخ والوقت')

    def __str__(self):
        return self.title + ' للكاتب: ' + self.profile.name
