from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError
from django.contrib import messages
from .models import Room, Booking
from django.utils.dateparse import parse_date
from datetime import date
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from .forms import UserRegisterForm
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required

import os
from config.settings import EMAIL_HOST_USER

from config.settings import EMAIL_HOST_USER



def index(request):
    return render(request, 'booking/index.html')


def room_list(request):

    Booking.objects.filter(end_date__lt=date.today()).delete()

    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')
    start_date = parse_date(start_date_str) if start_date_str else None
    end_date = parse_date(end_date_str) if end_date_str else None

    rooms = Room.objects.filter(is_active=True)
    today = date.today()

    if start_date and end_date:
        booked_rooms_ids = Booking.objects.filter(
            is_confirmed=True,
            end_date__gte=today,
            start_date__lt=end_date,
            end_date__gt=start_date
        ).values_list('room_id', flat=True)
        rooms = rooms.exclude(id__in=booked_rooms_ids)

    if request.method == 'POST':
        try:
            room = Room.objects.get(id=request.POST['room_id'])
            number_of_guests = int(request.POST['number_of_guests'])


            user_name = request.user.username if request.user.is_authenticated else request.POST['user_name']
            user_email = request.user.email if request.user.is_authenticated else request.POST['user_email']

            booking = Booking.objects.create_booking(
                user_name=user_name,
                user_email=user_email,
                room=room,
                start_date=request.POST['start_date'],
                end_date=request.POST['end_date'],
                number_of_guests=number_of_guests,
                is_confirmed=True,
            )


            send_mail(
                subject='Підтвердження бронювання',
                message=f'Дякуємо, {booking.user_name}! Ваше бронювання кімнати "{booking.room.name}" з {booking.start_date} по {booking.end_date} підтверджено.',
                from_email=EMAIL_HOST_USER,
                recipient_list=[booking.user_email],
                fail_silently=False,
            )

            messages.success(request, 'Бронювання успішно створено та підтверджено!')
        except (Room.DoesNotExist, ValidationError) as e:
            messages.error(request, f'Помилка: {e}')

        return redirect('booking:room-list')

    return render(request, 'booking/room_list.html', {
        'rooms': rooms,
        'start_date': start_date_str,
        'end_date': end_date_str
    })


def booking_list(request):
    bookings = Booking.objects.all().order_by('-created_at')
    return render(request, 'booking/booking_list.html', {'bookings': bookings})


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Ви успішно зареєструвались!")
            return redirect('booking:index')
    else:
        form = UserRegisterForm()
    return render(request, 'booking/register.html', {'form': form})



def booking_confirm(request):
    if request.method == 'POST':
        pass

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username, email=email)
            if check_password(password, user.password):
                login(request, user)
                messages.success(request, f'Вітаємо, {user.username}!')
                return redirect('booking:index')
            else:
                messages.error(request, 'Невірний пароль.')
        except User.DoesNotExist:
            messages.error(request, 'Користувача з такими даними не знайдено.')

    return render(request, 'booking/login.html')

