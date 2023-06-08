from django.urls import path
from . import views

app_name = 'my_auth'

urlpatterns = [
    path('login/', views.mylogin, name='login'),
    path('logout/', views.mylogout, name='logout')
]