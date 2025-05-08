from django.contrib import admin
from .models import Room, Booking, Availability

admin.site.register(Room)
admin.site.register(Booking)
admin.site.register(Availability)