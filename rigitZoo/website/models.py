from django.db import models

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
