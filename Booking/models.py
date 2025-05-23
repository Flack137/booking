from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError

class Room(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    capacity = models.IntegerField()
    price_per_night = models.DecimalField(max_digits=8, decimal_places=2)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def is_available(self, start_date, end_date):
        overlapping = self.bookings.filter(
            is_confirmed=True,
            start_date__lt=end_date,
            end_date__gt=start_date
        )
        return not overlapping.exists()


class BookingManager(models.Manager):
    def create_booking(self, **kwargs):
        start_date = kwargs.get('start_date')
        end_date = kwargs.get('end_date')
        room = kwargs.get('room')

        if start_date >= end_date:
            raise ValidationError("Дата закінчення має бути пізніше дати початку")

        if not room.is_available(start_date, end_date):
            raise ValidationError("Кімната недоступна для вибраних дат")

        return super().create(**kwargs)


class Booking(models.Model):
    user_name = models.CharField(max_length=100)
    user_email = models.EmailField()
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='bookings')
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(default=timezone.now)
    is_confirmed = models.BooleanField(default=False)

    objects = BookingManager()

    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(start_date__lt=models.F('end_date')), name='start_date_before_end_date')
        ]

    def __str__(self):
        return f"{self.user_name} - {self.room.name} ({self.start_date} → {self.end_date})"