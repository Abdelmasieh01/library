from django.urls import path
from . import views

app_name = 'my-auth'

urlpatterns = [
    path('web-auth/login/', views.mylogin, name='login'),
    path('web-auth/logout/', views.mylogout, name='logout'),
    path('web-auth/create-profile/', views.create_profile, name='create-profile'),
    path('my-account/', views.my_account, name='my-account'),
    path('my-account/change-password/', views.CustomPasswordChangeView.as_view(), name='change-password'),
    path('my-account/change-photo/', views.PorfilePhotoChangeView.as_view(), name='change-photo'),
]
