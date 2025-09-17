from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
import requests
from .forms import LoginForm, CreateUserForm

# Create your views here.
def home(request):
    return render(request, 'pages/index.html')

def weather_data(request):
    if request.method == "POST":
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

        context = {'data': data}

        return render(request, 'pages/index.html', context=context)
    else:
        return render(request, 'pages/index.html')

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
    return render(request, 'pages/booking/hotel.html')

@login_required(login_url="login")
def booking_day(request):
    return render(request, 'pages/booking/day.html')
