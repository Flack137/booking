from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError
from django.contrib import messages
from .models import Room, Booking


def index(request):
    return render(request, 'booking/index.html')


def room_list(request):
    rooms = Room.objects.filter(is_active=True)

    if request.method == 'POST':
        try:
            room = Room.objects.get(id=request.POST['room_id'])
            booking = Booking.objects.create_booking(
                user_name=request.POST['user_name'],
                user_email=request.POST['user_email'],
                room=room,
                start_date=request.POST['start_date'],
                end_date=request.POST['end_date'],
                is_confirmed=True,
            )
            messages.success(request, 'Бронювання успішно створено!')
        except (Room.DoesNotExist, ValidationError) as e:
            messages.error(request, f'Помилка: {e}')

        return redirect('booking:room-list')

    return render(request, 'booking/room_list.html', {'rooms': rooms})


def booking_list(request):
    bookings = Booking.objects.all().order_by('-created_at')
    return render(request, 'booking/booking_list.html', {'bookings': bookings})
