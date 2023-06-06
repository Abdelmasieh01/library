from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('books.urls')),
    path('posts/', include('posts.urls')),
    path('api/', include('api.urls')),
    path('auth/', include('dj_rest_auth.urls'))
]