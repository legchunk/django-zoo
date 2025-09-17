from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name=''),
    path('', views.weather_data, name=''),
    path('about', views.about, name='about'),
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('logout', views.user_logout, name='logout'),
    path('booking/hotel', views.booking_hotel, name='hotel'),
    path('booking/day', views.booking_day, name='day')
]
