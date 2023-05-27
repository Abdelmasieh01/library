from django.contrib import admin
from .models import *

admin.site.site_header = 'St. Peter Library'
admin.site.index_title = 'Library Administration'
admin.site.site_title = 'St. Peter Library'

# Register your models here.
class BookAdmin(admin.ModelAdmin):
    list_display = ('category', 'code', 'name', 'author', )

class BorrowerAdmin(admin.ModelAdmin):
    list_display = ('name', 'book_count')

    def book_count(self, obj):
        return obj.books.count()

class BorrowingAdmin(admin.ModelAdmin):
    list_display = ('borrower', 'book', 'borrow_date', 'return_date')


admin.site.register(Book, BookAdmin)
admin.site.register(Borrower, BorrowerAdmin)
admin.site.register(Borrowing, BorrowingAdmin)