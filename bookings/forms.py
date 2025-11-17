from django import forms
from .models import Booking, Guest, RoomType, Room
from django.forms import DateInput

class GuestForm(forms.ModelForm):
    class Meta:
        model = Guest
        fields = ["first_name", "last_name", "email", "phone"]

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ["room", "check_in", "check_out", "special_request"]
        widgets = {
            "check_in": DateInput(attrs={"type": "date"}),
            "check_out": DateInput(attrs={"type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only show active rooms
        self.fields["room"].queryset = Room.objects.filter(is_active=True)
