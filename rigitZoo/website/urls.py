from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name=''),
    path('about', views.about, name='about'),
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('logout', views.user_logout, name='logout'),
    path('booking', views.booking, name='booking'),
    path('booking/hotel', views.booking_hotel, name='hotel'),
    path('booking/day', views.booking_day, name='day'),
    path('booking/pay/', views.pay, name='pay'),
    path('booking/ticket/<str:code>/', views.ticket_view, name='ticket'),
    path('booking/my-tickets/', views.user_tickets, name='my_tickets'),
    path('events/fireworks', views.fireworks, name='fireworks'),
    path('events/santa', views.santa, name='santa')
]