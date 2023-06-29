from django.contrib import admin
from .models import *

admin.site.site_header = 'St. Peter Library'
admin.site.index_title = 'Library Administration'
admin.site.site_title = 'St. Peter Library'

# Register your models here.
class BookAdmin(admin.ModelAdmin):
    list_display = ('category', 'code', 'name', 'author', )

class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ('title',)

class BorrowingAdmin(admin.ModelAdmin):
    list_display = ('borrower', 'book', 'borrow_date', 'returned', 'return_date')
    list_editable = ('returned', 'return_date',)

class RecommendationAdmin(admin.ModelAdmin):
    list_display = ('book', 'title', 'timestamp',)

class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'show',)
    list_editable = ('show',)

admin.site.register(Book, BookAdmin)
admin.site.register(Borrowing, BorrowingAdmin)
admin.site.register(Recommendation, RecommendationAdmin)
admin.site.register(Announcement, AnnouncementAdmin)
admin.site.register(Subcategory, SubcategoryAdmin)