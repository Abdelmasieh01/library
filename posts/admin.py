from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Post, Profile


# Register your models here.
class ProfileAdmin(admin.ModelAdmin):
    pass

class PostAdmin(admin.ModelAdmin):
    list_display = ('profile', 'title', 'approved', 'timestamp',)
    list_editable = ['approved']
    change_list_template = 'posts/admin_change_list.html'
    
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Post, PostAdmin)