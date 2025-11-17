from django.urls import path
from . import views

urlpatterns = [
    path("", views.room_list, name="room_list"),
    path("room/<int:pk>/", views.room_detail, name="room_detail"),
    path("room/<int:pk>/<int:year>/<int:month>/", views.room_detail, name="room_detail_month"),
    path('book/<int:pk>/', views.book_room, name='book_room'),
    path("booking/<int:pk>/confirm/", views.booking_confirm_view, name="booking_confirm"),
    path("available-rooms/", views.room_availability, name="room_availability"),
    
]
