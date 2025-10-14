from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class HotelBooking(models.Model):
    booking_id = models.AutoField(primary_key=True, editable=False)
    # hotel_user_id = models.ForeignKey(ZooUser, on_delete=models.CASCADE)
    hotel_booking_date = models.DateField(auto_now_add=True)
    hotel_booking_date_arrive = models.DateField()
    hotel_booking_date_leave = models.DateField()
    hotel_booking_adults = models.IntegerField(default=0)
    hotel_booking_children = models.IntegerField(default=0)
    hotel_booking_oap = models.IntegerField(default=0)
    hotel_total_cost = models.FloatField(default=0)
    hotel_points = models.IntegerField(default=0)

class DayBooking(models.Model):
    booking_id = models.AutoField(primary_key=True, editable=False)
    day_booking_date_of_purchase = models.DateField(auto_now_add=True)
    day_booking_date = models.DateField()
    day_booking_adults = models.IntegerField(default=0)
    day_booking_children = models.IntegerField(default=0)
    day_booking_oap = models.IntegerField(default=0)
    day_total_cost = models.FloatField(default=0)
    day_points = models.IntegerField(default=0)

class ZooUser(AbstractUser):
    points = models.IntegerField(default=0)
    address = models.CharField(max_length=200, blank=True)
    phone = models.CharField(max_length=14)
    date_of_birth = models.DateField()
    full_name = models.CharField(max_length=100)

class Checkout(models.Model):
    billing_name = models.CharField(max_length=200)
    billing_address = models.CharField(max_length=200)
    billing_postcode = models.CharField(max_length=6)
    billing_city = models.CharField(max_length=200)
    card_num = models.CharField(max_length=16)
    card_expiry = models.DateField()
    card_cvv = models.CharField(max_length=4)