from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import ZooUser, HotelBooking
from django.forms.widgets import PasswordInput, TextInput

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput())
    password = forms.CharField(widget=PasswordInput())

class CreateUserForm(UserCreationForm):

    class Meta:
        model = ZooUser
        fields = ['username','password1','password2']

class HotelBookingForm(forms.ModelForm):
    class Meta:
        model = HotelBooking

        fields = ['hotel_booking_date_arrive','hotel_booking_date_leave','hotel_booking_adults',
            'hotel_booking_children','hotel_booking_oap','hotel_total_cost','hotel_points']

        labels = {
            "hotel_booking_date_arrive": 'Date of arrival',
        }
        widgets = {
            'hotel_booking_date_arrive': forms.DateInput(attrs={'type': 'date'}),
            'hotel_booking_date_leave': forms.DateInput(attrs={'type': 'date'}),
            'hotel_total_cost': forms.HiddenInput(),
            'hotel_points': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
