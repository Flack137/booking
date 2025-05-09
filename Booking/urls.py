from django.urls import path
from .views import room_list, booking_list, availability_list

urlpatterns = [
    path('rooms/', room_list, name='room-list'),
    path('bookings/', booking_list, name='booking-list'),
    path('availability/', availability_list, name='availability-list'),
]
