
from django.contrib import admin
from django.urls import path, include
from user import views

urlpatterns = [
    path('', views.login, name='home'),
    path('login', views.login, name='login'),
    path('register', views.register, name='register'),
    path('signin', views.signedin, name='signin')

 
]
