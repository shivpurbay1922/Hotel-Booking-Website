from django.contrib import admin
from .models import RoomType, Room, Pricing, Guest, Booking

@admin.register(RoomType)
class RoomTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "capacity")

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ("room_number", "room_type", "is_active")
    list_filter = ("room_type", "is_active")

@admin.register(Pricing)
class PricingAdmin(admin.ModelAdmin):
    list_display = ("room_type", "date", "price")
    list_filter = ("room_type",)

@admin.register(Guest)
class GuestAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "email", "phone")

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("id", "room", "guest", "check_in", "check_out", "created_at")
    list_filter = ("room__room_type",)
