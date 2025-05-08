from django.shortcuts import render
from .models import Room, Booking, Availability


def room_list(request):
    rooms = Room.objects.all()
    return render(request, 'rooms/list.html', {'rooms': rooms})


def booking_list(request):
    bookings = Booking.objects.all()
    return render(request, 'bookings/list.html', {'bookings': bookings})


def availability_list(request):
    availability = Availability.objects.all()
    return render(request, 'availability/list.html', {'availability': availability})

# Create your views here.
