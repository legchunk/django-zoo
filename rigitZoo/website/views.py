from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
import requests
from .forms import HotelBookingForm, DayBookingForm, LoginForm, CreateUserForm

# Create your views here.
def home(request):
    return render(request, 'pages/index.html')

def booking(request):
    return render(request, 'pages/booking.html')

def weather_data():
    key = settings.MY_API_KEY

    BASE_URL = "http://api.openweathermap.org/data/2.5/weather?q="

    city = "London"

    url = BASE_URL + 'London' + "&appid=" + key

    json_data = requests.get(url).json()

    weather = json_data['weather'][0]['main']
    temperature = int(json_data['main']['temp'] - 273.15)
    min = int(json_data['main']['temp_min'] - 273.15)
    max = int(json_data['main']['temp_max'] - 273.15)
    icon = json_data['weather'][0]['icon']

    data = {
        'location': city,
        'weather': weather,
        "temperature": temperature,
        "min": min,
        "max": max,
        "icon": icon
    }
    print(json_data)

    context = {'data': data}

    return context

def about(request):
    return render(request, 'pages/about.html')

def register(request):
    form = CreateUserForm()

    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')

    context = {"form": form}

    return render(request, 'pages/register.html', context=context)

def login(request):
    form = LoginForm()

    if request.method == "POST":
        form = LoginForm(request, data=request.POST)

        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                auth_login(request, user)
                return redirect('')  # Redirect to home page after successful login
            else:
                messages.error(request, 'Invalid username or password')

    context = {"form": form}
    return render(request, 'pages/login.html', context=context)


@login_required(login_url="login")
def user_logout(request):
    logout(request)
    return redirect('')

@login_required(login_url="login")
def booking_hotel(request):
    form = HotelBookingForm()
    if request.method == "POST":
        if request.is_valid():
            updated_request = request.POST.copy()
            updated_request.update({'hotel_user_id_id': request.user})

            form = HotelBookingForm(updated_request)

            if form.is_valid():
                obj = form.save(commit=False)

                arrive = obj.hotel_booking_date_arrive
                depart = obj.hotel_booking_date_leave
                result = depart - arrive
                print("Number of days: ", result.days)

                hotel_total_cost = int(obj.hotel_booking_adults) * 75 \
                    + int(obj.hotel_booking_children) * 35 \
                    + int(obj.hotel_booking_oap) * 40

                hotel_total_cost *= int(result.days)
                hotel_points = int(hotel_total_cost / 20)
                print("Hotel Points: ", hotel_points)

                obj.hotel_points = hotel_points
                obj.hotel_total_cost = hotel_total_cost
                obj.hotel_user_id = request.user

                obj.save()

                messages.success(request, "Hotel booked successfully!")
                return redirect('')
            else:
                print("There was a problem, try again later")
                return redirect('hotel')

    context = {'form': form}

    return render(request, 'pages/booking/hotel.html', context=context)

@login_required(login_url="login")
def booking_day(request):
    form = DayBookingForm()
    if request.method == "POST":
        form = DayBookingForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            
            # Calculate total cost
            day_total_cost = int(obj.day_booking_adults) * 25 \
                + int(obj.day_booking_children) * 15 \
                + int(obj.day_booking_oap) * 20
            
            day_points = int(day_total_cost / 10)
            
            obj.day_total_cost = day_total_cost
            obj.day_points = day_points
            # obj.day_user_id = request.user  # Add this if you have user relation
            
            obj.save()
            
            messages.success(request, "Day pass booked successfully!")
            return redirect('')
        else:
            messages.error(request, "There was a problem with your booking. Please try again.")
    
    context = {'form': form}
    return render(request, 'pages/booking/day.html', context=context)