from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError
from django.contrib import messages
from .models import Room, Booking
from datetime import date
from django.db.models import Q


def index(request):
    return render(request, 'booking/index.html')


def room_list(request):
    today = date.today()

    # Получаем комнаты, которые активны
    active_rooms = Room.objects.filter(is_active=True)

    # Фильтруем комнаты, у которых нет бронирований, пересекающихся с сегодняшним днем
    busy_rooms = Booking.objects.filter(
        Q(start_date__lte=today),
        Q(end_date__gte=today),
        is_confirmed=True
    ).values_list('room_id', flat=True)

    # Оставляем только те комнаты, которые не заняты сегодня
    free_rooms = active_rooms.exclude(id__in=busy_rooms)

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

    return render(request, 'booking/room_list.html', {'rooms': free_rooms})


def booking_list(request):
    bookings = Booking.objects.all().order_by('-created_at')
    return render(request, 'booking/booking_list.html', {'bookings': bookings})
