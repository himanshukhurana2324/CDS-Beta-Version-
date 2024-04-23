
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView
from user import views as user_views
from home import views as home_views

urlpatterns = [
    
    path('', RedirectView.as_view(url='home/', permanent=True), name='home'),
    path('login', user_views.login, name='login'),
    path('register', user_views.register, name='register'),
    path('signin', user_views.signedin, name='signin'),
    
]
