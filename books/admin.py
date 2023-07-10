from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.core.mail import EmailMultiAlternatives, send_mail
from django.contrib import messages
from datetime import datetime, timedelta
from .models import *

admin.site.site_header = 'St. Peter Library'
admin.site.index_title = 'Library Administration'
admin.site.site_title = 'St. Peter Library'

class LateReturnFilter(admin.SimpleListFilter):
    title = _('فلترة الاستعارات')
    parameter_name = 'return_filter'

    def lookups(self, request, model_admin):
        return (
            ('late', _('الاستعارات المتأخرة')),
            ('unreturned', _('لم يتم إرجاعها بعد')),
        )
    def queryset(self, request, queryset):
        if self.value() == 'late':
            return queryset.filter(returned=False, borrow_date__lte=datetime.now().date() - timedelta(days=15))
        
        if self.value() == 'unreturned':
            return queryset.filter(returned=False,)

@admin.action(description=('إرسال إيميلات للاستعارات المختارة'))
def send_late_return_email(model_admin, request, queryset):
    for borrowing in queryset:
        recipient = borrowing.borrower.user.email
        try:
            if recipient and recipient != '':
                msg = EmailMultiAlternatives(
                    subject='لقد تأخرت في إرجاع كتاب للمكتبة!', 
                    body=f'لقد تأخرت في إرجاع كتاب {borrowing.book.name}',
                    from_email='St. Peter Library <stpeterlibrary39@gmail.com>', 
                    to=[recipient])
                msg.send(fail_silently=False)
            else:
                messages.error(request, f'البريد الإلكتروني ل{borrowing.borrower.name} غير مسجل')
        except:
            messages.error(request, f'{borrowing.borrower.name} فشل إرسال رسالة إلى')

# Register your models here.
class BookAdmin(admin.ModelAdmin):
    list_display = ('category', 'code', 'name', 'author', )

class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ('title',)

class BorrowingAdmin(admin.ModelAdmin):
    list_display = ('borrower', 'book', 'borrow_date', 'returned', 'return_date')
    list_editable = ('returned', 'return_date',)
    list_filter = (LateReturnFilter,)
    actions = [send_late_return_email]

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