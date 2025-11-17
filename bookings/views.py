from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from datetime import date, timedelta
import calendar
from .models import RoomType, Room, Booking, Pricing, Guest
from .forms import BookingForm
 
 
def room_list(request):
    
    available_rooms = Room.objects.filter(is_active=True)
    return render(request, 'bookings/room_list.html', {'rooms': available_rooms})


def room_detail(request, pk, year=None, month=None):
    
    room_type = get_object_or_404(RoomType, pk=pk)
    today = date.today()
    year = year or today.year
    month = month or today.month

    cal = calendar.Calendar()
    month_days = []
    for week in cal.monthdatescalendar(year, month):
        week_data = []
        for day in week:
            booked = Booking.objects.filter(
                room__room_type=room_type,
                check_in__lte=day,
                check_out__gt=day
            ).exists()
            price_obj = Pricing.objects.filter(room_type=room_type, date=day).first()
            price = price_obj.price if price_obj else None
            week_data.append({
                "day": day, "current_month": day.month == month, "booked": booked, "price": price
            })
        month_days.append(week_data)

    prev_month = (date(year, month, 1) - timedelta(days=1)).replace(day=1)
    next_month = (date(year, month, 28) + timedelta(days=4)).replace(day=1)

    return render(request, "bookings/room_detail.html", {
        "room_type": room_type,
        "month_days": month_days,
        "year": year, "month": month,
        "prev_year": prev_month.year, "prev_month": prev_month.month,
        "next_year": next_month.year, "next_month": next_month.month,
    })


 

@login_required
def book_room(request, pk):
    room = get_object_or_404(Room, pk=pk)

    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)

            # Validate date inputs
            if booking.check_in < date.today():
                messages.error(request, "❌ Check-in date cannot be before today.")
                return redirect("book_room", pk=room.pk)
            if booking.check_in >= booking.check_out:
                messages.error(request, "❌ Check-out date must be after check-in date.")
                return redirect("book_room", pk=room.pk)

            # Check if the room is already booked for those dates
            overlap = Booking.objects.filter(
                room=room,
                check_in__lt=booking.check_out,
                check_out__gt=booking.check_in
            ).exists()
            if overlap:
                messages.error(request, "⚠️ This room is already booked for the selected dates.")
                return redirect("book_room", pk=room.pk)

            # Get or create Guest from the logged-in user
            guest, _ = Guest.objects.get_or_create(
                email=request.user.email,
                defaults={
                    "first_name": request.user.first_name or request.user.username,
                    "last_name": request.user.last_name or "",
                    "phone": "",
                }
            )
            booking.guest = guest
            booking.room = room

            # Calculate base room cost
            total = 0
            day = booking.check_in
            while day < booking.check_out:
                price_record = Pricing.objects.filter(room_type=room.room_type, date=day).first()
                total += float(price_record.price) if price_record else float(room.price_per_night)
                day += timedelta(days=1)

            # Add-on services
            selected_services = request.POST.getlist("services")
            service_prices = {
                "gym": 500,
                "spa": 700,
                "pool": 400,
            }
            for service in selected_services:
                total += service_prices.get(service, 0)

            # Handle payment option
            payment_option = request.POST.get("payment_option", "Pay Later")
            booking.payment_option = payment_option  # Save this field in your model if not yet added

            booking.total_amount = total
            booking.save()

            if payment_option == "Pay Now":
                messages.success(request, f"✅ Room booked successfully! You chose to pay now. Total ₹{total}.")
            else:
                messages.success(request, f"✅ Room booked successfully! Pay ₹{total} later at check-in.")

            return redirect("booking_confirm", pk=booking.pk)
    else:
        form = BookingForm()

    return render(request, "bookings/book_room.html", {"form": form, "room": room})




@login_required
def booking_confirm_view(request, pk):
    """Confirm booking and show total cost."""
    booking = get_object_or_404(Booking, pk=pk)
    total = 0
    day = booking.check_in
    while day < booking.check_out:
        p = Pricing.objects.filter(room_type=booking.room.room_type, date=day).first()
        if p:
            total += float(p.price)
        day += timedelta(days=1)
    return render(request, "bookings/booking_confirm.html", {"booking": booking, "total": total})


@login_required
def room_availability(request):
    """Show all available rooms with images and details."""
    rooms = Room.objects.filter(is_active=True)
    return render(request, 'bookings/room_availability.html', {'rooms': rooms})
