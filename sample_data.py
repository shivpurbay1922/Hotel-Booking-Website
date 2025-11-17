# Run this with: python sample_data.py
import os
import django
from datetime import date, timedelta

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hotel_booking.settings")
django.setup()

from bookings.models import RoomType, Room, Pricing

def run():
    rt1, _ = RoomType.objects.get_or_create(name="Standard", defaults={"description":"Cozy standard room","capacity":2})
    rt2, _ = RoomType.objects.get_or_create(name="Deluxe", defaults={"description":"Larger and nicer","capacity":3})
    Room.objects.get_or_create(room_number="101", room_type=rt1)
    Room.objects.get_or_create(room_number="102", room_type=rt1)
    Room.objects.get_or_create(room_number="201", room_type=rt2)

    # Add prices for the next 30 days
    start = date.today()
    for i in range(0, 30):
        d = start + timedelta(days=i)
        Pricing.objects.get_or_create(room_type=rt1, date=d, defaults={"price": 2500.00})
        Pricing.objects.get_or_create(room_type=rt2, date=d, defaults={"price": 4000.00})
    print("Sample data created.")

if __name__ == "__main__":
    run()
