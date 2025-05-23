from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError
from django.contrib import messages
from .models import Room, Booking
from datetime import date
from django.db.models import Q
from django.utils.dateparse import parse_date


def index(request):
    return render(request, 'booking/index.html')


def room_list(request):
    selected_date_str = request.GET.get('date')
    selected_date = parse_date(selected_date_str) if selected_date_str else None
    rooms = Room.objects.filter(is_active=True)

    if selected_date:
        booked_rooms_ids = Booking.objects.filter(
            is_confirmed=True,
            start_date__lte=selected_date,
            end_date__gte=selected_date
        ).values_list('room_id', flat=True)
        rooms = rooms.exclude(id__in=booked_rooms_ids)

    if request.method == 'POST':
        try:
            room = Room.objects.get(id=request.POST['room_id'])
            number_of_guests = int(request.POST['number_of_guests'])

            booking = Booking.objects.create_booking(
                user_name=request.POST['user_name'],
                user_email=request.POST['user_email'],
                room=room,
                start_date=request.POST['start_date'],
                end_date=request.POST['end_date'],
                number_of_guests=number_of_guests,
                is_confirmed=True,
            )
            messages.success(request, 'Бронювання успішно створено!')
        except (Room.DoesNotExist, ValidationError) as e:
            messages.error(request, f'Помилка: {e}')

        return redirect('booking:room-list')

    return render(request, 'booking/room_list.html', {
        'rooms': rooms,
        'selected_date': selected_date_str
    })


def booking_list(request):
    bookings = Booking.objects.all().order_by('-created_at')
    return render(request, 'booking/booking_list.html', {'bookings': bookings})
