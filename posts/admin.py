from django.contrib import admin
from .models import Post, Profile


# Register your models here.
class ProfileAdmin(admin.ModelAdmin):
    pass

class PostAdmin(admin.ModelAdmin):
    list_display = ('profile', 'title', 'timestamp')

admin.site.register(Profile, ProfileAdmin)
admin.site.register(Post, PostAdmin)