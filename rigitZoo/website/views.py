from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
import requests
from .forms import HotelBookingForm, DayBookingForm, LoginForm, CreateUserForm, CheckoutForm
from django.urls import reverse
from .models import Ticket
import secrets
import io
import base64
import qrcode

def home(request):
    return render(request, 'pages/index.html')

def booking(request):
    return render(request, 'pages/booking.html')

def about(request):
    return render(request, 'pages/about.html')

def education(request):
    return render(request, 'pages/events/santa.html')

def ticket(request):
    return render(request, 'pages/booking/ticket.html')

def fireworks(request):
    return render(request, 'pages/events/fireworks.html')

def santa(request):
    return render(request, 'pages/events/santa.html')

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
        form = HotelBookingForm(request.POST)
        if form.is_valid():
            updated_request = request.POST.copy()
            updated_request.update({'hotel_user_id_id': request.user})

            form = HotelBookingForm(updated_request)

            print(form.errors)

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

                # Store a small booking summary in session for the ticket page
                request.session['pending_booking'] = {
                    'type': 'hotel',
                    'adults': int(obj.hotel_booking_adults),
                    'children': int(obj.hotel_booking_children),
                    'seniors': int(obj.hotel_booking_oap),
                    'arrive': obj.hotel_booking_date_arrive.isoformat(),
                    'leave': obj.hotel_booking_date_leave.isoformat(),
                    'nights': result.days,
                    'total_cost': float(obj.hotel_total_cost),
                }

                messages.success(request, "Hotel booked successfully!")
                # Redirect to payment so user can complete payment and receive a ticket
                return redirect('pay')
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
            
            # Store a small booking summary in session for the ticket page
            request.session['pending_booking'] = {
                'type': 'day',
                'date': obj.day_booking_date.isoformat(),
                'adults': int(obj.day_booking_adults),
                'children': int(obj.day_booking_children),
                'seniors': int(obj.day_booking_oap),
                'total_cost': float(obj.day_total_cost),
            }
            
            return redirect('pay')
        else:
            messages.error(request, "There was a problem with your booking. Please try again.")
    
    context = {'form': form}
    return render(request, 'pages/booking/day.html', context=context)

def pay(request):
	"""
	Display CheckoutForm and on valid POST:
	- generate unique ticket code and create Ticket (assigned to request.user if logged in)
	- save Checkout record with ticket attached
	- generate QR PNG and return ticket template with base64 image
	"""
	if request.method == 'POST':
		form = CheckoutForm(request.POST)
		if form.is_valid():
			# generate a short URL-safe random string and create Ticket first
			code = secrets.token_urlsafe(8)
			while Ticket.objects.filter(code=code).exists():
				code = secrets.token_urlsafe(8)
			# assign ticket to current user when available
			ticket = Ticket.objects.create(code=code, valid=True, user=request.user if request.user.is_authenticated else None)

			# save billing info and attach ticket to checkout
			checkout = form.save(ticket=ticket)

			# generate QR image into memory
			qr_img = qrcode.make(code)
			buffer = io.BytesIO()
			qr_img.save(buffer, format='PNG')
			qr_b64 = base64.b64encode(buffer.getvalue()).decode('ascii')

			# retrieve pending booking summary from session (if any) and remove it
			pending = request.session.pop('pending_booking', None)

			# render ticket with QR embedded and booking info
			return render(request, 'pages/booking/ticket.html', {'qr_data': qr_b64, 'ticket_code': code, 'ticket_info': pending})
	else:
		form = CheckoutForm()
	return render(request, 'pages/booking/pay.html', {'form': form})

@login_required(login_url="login")
def user_tickets(request):
	"""
	Show all tickets that belong to the currently logged in user.
	Each ticket includes a small inline QR (base64) for quick display and a link to view the full ticket.
	"""
	tickets = Ticket.objects.filter(user=request.user).order_by('-created_at')

	qr_items = []
	for t in tickets:
		# create QR image for each ticket
		qr_img = qrcode.make(t.code)
		buffer = io.BytesIO()
		qr_img.save(buffer, format='PNG')
		qr_b64 = base64.b64encode(buffer.getvalue()).decode('ascii')
		qr_items.append({
			'ticket': t,
			'qr_b64': qr_b64,
		})

	return render(request, 'pages/booking/my_tickets.html', {'qr_items': qr_items})

def ticket_view(request, code):
	"""
	Render a ticket QR for an existing ticket code.
	"""
	try:
		ticket = Ticket.objects.get(code=code)
	except Ticket.DoesNotExist:
		return render(request, 'pages/booking/ticket.html', {'error': 'Ticket not found'})

	qr_img = qrcode.make(ticket.code)
	buffer = io.BytesIO()
	qr_img.save(buffer, format='PNG')
	qr_b64 = base64.b64encode(buffer.getvalue()).decode('ascii')
	return render(request, 'pages/booking/ticket.html', {'qr_data': qr_b64, 'ticket_code': ticket.code})

