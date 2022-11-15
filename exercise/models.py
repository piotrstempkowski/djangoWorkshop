from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
class ConferenceRoom(models.Model):
    name = models.CharField(max_length=255, unique=True)
    capacity = models.PositiveIntegerField()
    projector_availability = models.BooleanField(default=False)


class RoomReservation(models.Model):
    # Jedna sali może mieć wiele całodniowych rezerwacji
    room = models.ForeignKey(ConferenceRoom, on_delete=models.CASCADE)
    date = models.DateField()
    comment = models.TextField(null=True)
    # Id sali połączona z data rezerwacji była unikalna
    class Meta:
        unique_together = ("room", "date")
