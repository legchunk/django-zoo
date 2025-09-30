from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import ZooUser, HotelBooking, DayBooking
from django.forms.widgets import PasswordInput, TextInput

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput())
    password = forms.CharField(widget=PasswordInput())

class CreateUserForm(UserCreationForm):
    phone = forms.CharField(
        max_length=14, 
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': '07505123456'
        }),
        help_text='Do not include country code (e.g., 07505123456)'
    )
    full_name = forms.CharField(
        max_length=100, 
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    date_of_birth = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={
            'type': 'date', 
            'class': 'form-control'
        })
    )

    class Meta:
        model = ZooUser
        fields = ['full_name', 'username', 'phone', 'date_of_birth', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.phone = self.cleaned_data['phone']
        user.full_name = self.cleaned_data['full_name']
        user.date_of_birth = self.cleaned_data['date_of_birth']
        if commit:
            user.save()
        return user

class UserModifyForm(forms.ModelForm):
    class Meta:
        model = ZooUser
        fields = ['username', 'first_name', 'last_name', 'email', 'address', 'phone']
        
        labels = {
            'username': 'Username',
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'email': 'Email Address',
            'address': 'Address',
            'phone': 'Phone Number',
        }
        
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+1234567890'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make email required
        self.fields['email'].required = True
        # Add help text for phone
        self.fields['phone'].help_text = 'Include country code (e.g., +1234567890)'

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

class DayBookingForm(forms.ModelForm):
    class Meta:
        model = DayBooking

        fields = ['day_booking_date','day_booking_adults',
            'day_booking_children','day_booking_oap','day_total_cost','day_points']

        labels = {
            "day_booking_date": 'Date',
        }
        widgets = {
            'day_booking_date': forms.DateInput(attrs={'type': 'date'}),
            'day_total_cost': forms.HiddenInput(),
            'day_points': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
