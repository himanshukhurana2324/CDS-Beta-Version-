from django.contrib import admin
from django.urls import path
from home import views

urlpatterns = [
    
    path('',views.dashboard ,name='home'),
    path('calculate',views.home, name='calulate'),
    path('output',views.output, name='output'),
    path('run_script/', views.run_script, name='run_script')
]