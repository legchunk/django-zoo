from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name=''),
    path('about', views.about, name='about'),
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('logout', views.user_logout, name='logout')
]
