from django.db import models
from books.models import Book

# Create your models here.
class Profile(models.Model):
    name = models.CharField(unique=True, verbose_name='الاسم', max_length=150)
    photo = models.URLField(blank=True, verbose_name='الصورة')

    def __str__(self):
        return self.name

class Post(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name='الكاتب')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, null=True, blank=True, verbose_name='الكتاب')
    title = models.CharField(max_length=255, verbose_name='العنوان')
    text = models.TextField(max_length=50000, verbose_name='النص')
    image = models.URLField(blank=True, verbose_name='الصورة')
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name='التاريخ والوقت')

    def __str__(self):
        return self.title + ' للكاتب: ' + self.profile.name