from django.urls import path
from . import views

app_name = 'my-auth'

urlpatterns = [
    path('login/', views.mylogin, name='login'),
    path('logout/', views.mylogout, name='logout'),
    path('create-profile/', views.create_profile, name='create-profile'),
    path('my-account/', views.my_account, name='my-account'),
    path('my-account/change-password/', views.CustomPasswordChangeView.as_view(), name='change-password'),
    path('my-account/change-photo/', views.PorfilePhotoChangeView.as_view(), name='change-photo'),
]
