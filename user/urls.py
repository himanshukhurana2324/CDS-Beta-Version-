
from django.contrib import admin
from django.urls import path, include
from user import views as user_views
from home import views as home_views

urlpatterns = [
    path('', home_views.dashboard, name='home'),
    path('login', user_views.login, name='login'),
    path('register', user_views.register, name='register'),
    path('signin', user_views.signedin, name='signin'),
  

]
