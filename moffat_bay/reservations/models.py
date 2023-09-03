from django.db import models
from users.models import CustomUser
from rooms.models import RoomChoices, Rooms

#stay costs model
class Stay_Costs(models.Model):
    guests = models.IntegerField(unique=True)
    price = models.DecimalField(decimal_places=2, max_digits=5)

    
    class Meta:
        verbose_name_plural = "Nightly Costs"

    def __str__(self):
        return f"{self.guests} guests per night: ${self.price}"



#reservations model - saving the actual reservations
#class Reservations(models.Model):
#    reservationID = models.IntegerField(primary_key=True, auto_created=True)
#    confirmationKey =models.CharField(max_length=8,  null=False)
#    userID = models.ForeignKey(Account, to_field='id', on_delete=models.PROTECT)
#    roomID = models.ForeignKey(Rooms, to_field='roomID', on_delete=models.PROTECT)
#    guests = models.IntegerField(default=1, max=5, null=False)
#    totalPrice = models.IntegerField(null=False)
#    checkInDate = models.DateField(null=False)
#    checkOutDate = models.DateField(null=False)

#add class meta, and return strings. 