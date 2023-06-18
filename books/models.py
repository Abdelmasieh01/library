from django.db import models
from django.contrib.auth.models import User


class Book(models.Model):
    MIX = 200
    FAMILY = 300
    YOUTH = 400
    SERVICE = 500
    SPIRITUAL = 600
    HISTORY = 700
    RITUAL = 800
    CREED = 900
    BIBLE = 1000
    ENCYCLOPEDIAS = 2000
    VOLUMES = 3000

    CATEGORIES = (
        (MIX, 'منوعات'),
        (FAMILY, 'الأسرة'),
        (YOUTH, 'الشباب'),
        (SERVICE, 'الخدمة'),
        (SPIRITUAL, 'اللاهوت الروحي'),
        (HISTORY, 'تاريخ الكنيسة وسير الآباء'),
        (RITUAL, 'اللاهوت الطقسي'),
        (CREED, 'اللاهوت العقائدي'),
        (BIBLE, 'الكتاب المقدس'),
        (ENCYCLOPEDIAS, 'الموسوعات'),
        (VOLUMES, 'المجلدات'),
    )

    AGE_CATEGORIES = (
        (1, 'حضانة'),
        (2, 'ابتدائي'),
        (3, 'اعدادي'),
        (4, 'ثانوي'),
        (5, 'الشباب'),
        (6, 'الأسرة'),
    )

    category = models.IntegerField(default=MIX, choices=CATEGORIES, verbose_name='الرقم العام')
    age_category = models.IntegerField(blank=True, null=True, choices=AGE_CATEGORIES, verbose_name='الفئة العمرية')
    code = models.IntegerField(verbose_name='الرقم الخاص')
    name = models.CharField(max_length=150, verbose_name='اسم الكتاب')
    author = models.CharField(max_length=150, verbose_name='المؤلف')
    copies = models.IntegerField(default=1, verbose_name='عدد النسخ')
    image = models.URLField(blank=True, null=True, verbose_name='صورة الكتاب')
    link = models.URLField(blank=True, null=True, verbose_name='رابط الكتاب')
    available = models.BooleanField(default=True, verbose_name='متاح')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['category', 'code'], name='unique_category_code')
        ]

    def __str__(self):
        return self.name + ' - ' + str(self.category) + ' - ' + str(self.code) + ' - ' + self.author

    

class Author(models.Model):
    pass

'''
class Borrower(models.Model):
    name = models.CharField(max_length=150, verbose_name='اسم المستعير', unique=True)
    books = models.ManyToManyField(Book, blank=True, verbose_name='الكتب التي استعارها')

    def __str__(self):
        return self.name + ': ' + str(self.count_books()) + ' كتاب'

    def count_books(self):
        return self.books.count()
'''
from posts.models import Profile
class Borrowing(models.Model):
    borrower = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name='المستعير')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name='الكتاب')
    borrow_date = models.DateField(verbose_name='تاريخ الاستعارة')
    return_date = models.DateField(blank=True, null=True, verbose_name='تاريخ الإرجاع')
    returned = models.BooleanField(default=False, verbose_name='تم الإرجاع')

    def __str__(self):
        return self.borrower.name() + ': ' + self.book.name
    
    def save(self, *args, **kwargs):
        if self.returned == False:
            self.book.copies -= 1
            self.book.available = (self.book.copies > 0)
            self.borrower.books.add(self.book)
            self.book.save()
            
        else:
            self.book.copies += 1
            self.book.available = True
            self.borrower.books.remove(self.book)
            self.book.save()

        super(Borrowing, self).save(*args, **kwargs)

class Recommendation(models.Model):
    book = models.OneToOneField(Book, on_delete=models.CASCADE, verbose_name='الكتاب')
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name='المستخدم')
    title = models.TextField(verbose_name='العنوان')
    text = models.TextField(verbose_name='النص')
    approved = models.BooleanField(default=False, verbose_name='قبول الاقتراح')
    timestamp = models.DateField(auto_now_add=True, verbose_name='التاريخ')

    def __str__(self) -> str:
        return 'ترشيح لكتاب: ' + self.book.name
