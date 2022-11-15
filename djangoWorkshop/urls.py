"""djangoWorkshop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from exercise.views import (
    HomeView,
    AddRoomView,
    RoomListView,
    DeleteRoomView,
    ModifyRoomView,
    ReservationView,
    RoomDetailView,
    RoomsAvailabilityView,
    ReservationsView,
    RoomSearch,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", HomeView.as_view(), name="base"),
    path("room/new/", AddRoomView.as_view(), name="add-room"),
    path("rooms/", RoomListView.as_view(), name="room-list"),
    path("room/delete/<int:room_id>/", DeleteRoomView.as_view(), name="delete-room"),
    path("room/modify/<int:room_id>/", ModifyRoomView.as_view(), name="modify_room"),
    path("room/reserve/<int:room_id>/", ReservationView.as_view(), name="reserve_room"),
    path(
        "room/reservation/<int:room_id>/", RoomDetailView.as_view(), name="reservation"
    ),
    path(
        "rooms/availability",
        RoomsAvailabilityView.as_view(),
        name="rooms",
    ),
    path(
        "room/reservation-form/<int:room_id>",
        ReservationsView.as_view,
        name="reservation_form",
    ),
    path("room/search", RoomSearch.as_view(), name="room-search"),
]
