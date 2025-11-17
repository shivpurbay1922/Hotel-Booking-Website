from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone

class RoomType(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    capacity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.name

from django.db import models
from django.utils import timezone

class Room(models.Model):
    room_number = models.CharField(max_length=20, unique=True)
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    image = models.ImageField(upload_to='room_images/', blank=True, null=True)
    description = models.TextField(blank=True)
    price_per_night = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.room_number} ({self.room_type.name})"
class Pricing(models.Model):
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE, related_name="pricings")
    date = models.DateField()
    price = models.DecimalField(max_digits=8, decimal_places=2)

    class Meta:
        unique_together = ("room_type", "date")

    def __str__(self):
        return f"{self.room_type.name} - {self.date}: {self.price}"

class Guest(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, blank=True)
    email = models.EmailField()
    phone = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}".strip()

class Booking(models.Model):
    room = models.ForeignKey(Room, on_delete=models.PROTECT, related_name="bookings")
    guest = models.ForeignKey(Guest, on_delete=models.CASCADE, related_name="bookings")
    check_in = models.DateField()
    check_out = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    special_request = models.TextField(blank=True)

    def clean(self):
        if self.check_in >= self.check_out:
            raise ValidationError("Check-out must be after check-in.")
        # check overlaps on same room
        overlap_qs = Booking.objects.filter(
            room=self.room,
            check_in__lt=self.check_out,
            check_out__gt=self.check_in
        )
        if self.pk:
            overlap_qs = overlap_qs.exclude(pk=self.pk)
        if overlap_qs.exists():
            raise ValidationError("This room is already booked for the selected dates.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def nights(self):
        return (self.check_out - self.check_in).days

    def __str__(self):
        return f"Booking #{self.pk} {self.room} for {self.guest} [{self.check_in} → {self.check_out}]"

class SpecialRequest(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name="special_requests")
    text = models.TextField()

    def __str__(self):
        return f"Request for {self.booking_id}"
 