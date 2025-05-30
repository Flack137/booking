from django.urls import path
from .views import index, room_list, booking_list, register

app_name = 'booking'

urlpatterns = [
    path('', index, name='index'),
    path('rooms/', room_list, name='room-list'),
    path('bookings/', booking_list, name='booking-list'),
    path('register/', register, name='register'),
]
