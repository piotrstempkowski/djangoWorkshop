from django.shortcuts import render, redirect
from .models import RoomReservation
import datetime

# Create your views here.
def base_view(request):
    return render(request, "exercise/base.html", {})


from .models import ConferenceRoom


def add_conference_room_view(request):
    if request.method == "GET":
        return render(request, "exercise/add_conf_room.html")
    else:
        name = request.POST.get("room-name")
        capacity = request.POST.get("capacity")
        capacity = int(capacity) if capacity else 0
        projector = request.POST.get("projector") == "on"
        if not name:
            return render(
                request,
                "exercise/add_conf_room.html",
                context={"error": "Name of conference room incorrect."},
            )
        if capacity <= 0:
            return render(
                request,
                "exercise/add_conf_room.html",
                context={"error": "Capacity of coference room must be positive"},
            )
        if ConferenceRoom.objects.filter(name=name).first():
            return render(
                request,
                "exercise/add_conf_room.html",
                context={
                    "error": "Name of conference room already exists in database."
                },
            )
        ConferenceRoom.objects.create(
            name=name, capacity=capacity, projector_availability=projector
        )
        return redirect("room-list")


# obsuzyc przypadek post


def room_list_view(request):
    if request.method == "GET":
        rooms = ConferenceRoom.objects.all()
        return render(request, "exercise/room.html", context={"rooms": rooms})


def delete_room(request, id):
    if request.method == "GET":
        ConferenceRoom.objects.get(id=id).delete()
        return redirect("room-list")


def modify_room(request, id):
    if request.method == "GET":
        room = ConferenceRoom.objects.get(id=id)
        return render(request, "exercise/delete_room.html", context={"room": room})
    else:
        room = ConferenceRoom.objects.get(id=id)
        name = request.POST.get("room-name")
        capacity = request.POST.get("capacity")
        capacity = int(capacity) if capacity else 0
        projector = request.POST.get("projector") == "on"
        if not name:
            return render(
                request,
                "exercise/modify_room.html",
                context={"error": "Name room is required."},
            )
        if capacity <= 0:
            return render(
                request,
                "exercise/modify-room.html",
                context={"error": "Room capacity must be postive"},
            )
        if ConferenceRoom.objects.filter(name=name).first() and room.name != name:
            return render(
                request,
                "exercise/modify_room.html",
                context={"error": "Conference room name can't duplicate."},
            )
        room.name = name
        room.capacity = capacity
        room.projector_availability = projector
        room.save()
        return redirect("room-list")


def room_reservatation_view(request, room_id):
    if request.method == "GET":
        room = ConferenceRoom.objects.get(id=room_id)
        return render(request, "exercise/reserve_room.html", context={"room": room})
    else:
        room = ConferenceRoom.objects.get(id=room_id)
        date = request.POST.get("reservation-date")
        comment = request.POST.get("comment")
        if RoomReservation.objects.filter(room_id=room, date=date):
            return render(
                request,
                "reserve_room.html",
                context={"error": "Room is already reserved."},
            )
        if date < str(datetime.date.today()):
            return render(
                request,
                "reserve_room.html",
                context={"error": "Date cannot be in the past"},
            )
        RoomReservation.objects.create(room_id=room, date=date, comment=comment)
        return redirect("room-list")


def reservation_view(request, room_id):
    if request.method == "GET":
        room = ConferenceRoom.objects.get(id=room_id)
        reservations = room.roomreservation_set.filter(
            date__gte=str(datetime.date.today())
        ).order_by("date")
        return render(
            request,
            "exercise/reservations.html",
            context={
                "room": room,
                "reservations": reservations,
            },
        )


def room_availability_view(request):
    if request.method == "GET":
        rooms = ConferenceRoom.objects.all()  # pobieram dane do salach
        for room in rooms:  # iteruje się po pokojach
            reservation_dates = [
                reservation.date for reservation in room.roomreservation_set.all()
            ]  # dla każej sali wyciągam daty kiedy jest zajea
            room.reserved = datetime.date.today() in reservation_dates
        return render(
            request, "exercise/rooms_availability.html", context={"rooms": rooms}
        )


def reservation_form_view(request, room_id):
    if request.method == "GET":
        room = ConferenceRoom.objects.get(id=room_id)
        reservations = room.roomreservation_set.filter(
            date__gte=str(datetime.date.today())
        ).order_by("date")
        return render(
            request,
            "exercise/reservation_form.html",
            context={"room": room, "reservations": reservations},
        )

    if request.method == "POST":
        room = ConferenceRoom.objects.get(id=room_id)
        date = request.POST.get("exercise/reservation-date")
        comment = request.POST.get("comment")

        reservations = room.roomreservation_set.filter(
            date__gte=str(datetime.date.today())
        ).order_by("date")

        if RoomReservation.objects.filter(room_id=room, date=date):
            return render(
                request,
                "exercise/reservation_form.html",
                context={
                    "room": room,
                    "reservations": reservations,
                    "error": "Sala jest już zarezerwowana!",
                },
            )
        if date < str(datetime.date.today()):
            return render(
                request,
                "exercise/reservation_form.html",
                context={
                    "room": room,
                    "reservations": reservations,
                    "error": "Data jest z przeszłości!",
                },
            )

        RoomReservation.objects.create(room_id=room, date=date, comment=comment)
        return redirect("room-list")


def room_search_view(request):
    if request.method == "GET":

        name = request.POST.get("room-name")
        capacity = request.POST.get("capacity")
        capacity = int(capacity) if capacity else 0
        projector = request.POST.get("projector") == "On"

        rooms = ConferenceRoom.objects.all()
        if projector:
            rooms = rooms.filter(projector_availability=projector)
        if capacity:
            rooms = rooms.filter(capacity__gte=capacity)
        if name:
            rooms = rooms.filter(name__contains=name)
        for room in rooms:
            reservation_dates = [
                reservation.date for reservation in room.roomreservation_set.all()
            ]
            room.reserved = str(datetime.date.today()) in reservation_dates

    return render(
        request,
        "exercise/room_search.html",
        context={"rooms": rooms, "date": datetime.date.today()},
    )
