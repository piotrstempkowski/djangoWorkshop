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
from django.urls import re_path
from exercise.views import (
base_view,
add_conference_room_view,
room_list_view,
delete_room,
modify_room,
room_reservatation_view,
reservation_view,
room_availability_view,
reservation_form_view,
room_search_view,)
urlpatterns = [
    path('admin/', admin.site.urls),
    path("base/", base_view, name="base"),
    path("room/new/", add_conference_room_view, name="add-room"),
    path("", room_list_view, name="room-list"),
    path("room/delete/<int:id>/", delete_room, name="delete-room"),
    path("room/modify/<int:id>/", modify_room, name="modify_room"),
    path("room/reserve/<int:room_id>/", room_reservatation_view, name="reserve_room"),
    path("room/reservation/<int:room_id>/", reservation_view, name="reservation"),
    path("rooms/availability", room_availability_view, name="rooms", ),
    path("room/reservation-form/<int:room_id>", reservation_form_view, name="reservation_form"),
    path("room/search", room_search_view, name="room-search"),
]
