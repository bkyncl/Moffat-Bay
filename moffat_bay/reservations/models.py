from django.db import models
from users.models import CustomUser
from rooms.models import RoomChoices, Rooms
from .utilities import *

#stay costs model
class Stay_Costs(models.Model):
    guests = models.IntegerField(unique=True)
    price = models.DecimalField(decimal_places=2, max_digits=5)

    
    class Meta:
        verbose_name_plural = "Nightly Costs"

    def __str__(self):
        return f"{self.guests} guests per night: ${self.price}" #this is listed in breadcrumbs on admin page
    

#reservations model - saving the actual reservations
class Reservations(models.Model):
    reservationID = models.IntegerField(primary_key=True, auto_created=True)
    confirmationKey =models.CharField(max_length=7, null=False)
    userID = models.ForeignKey(CustomUser, to_field='id', on_delete=models.PROTECT)
    roomID = models.ForeignKey(Rooms, to_field='roomID', on_delete=models.PROTECT)
    guests = models.IntegerField(default=1, null=False)
    totalPrice = models.DecimalField(null=False, decimal_places=2, max_digits=11)
    checkInDate = models.DateField(null=False)
    checkOutDate = models.DateField(null=False)

    class Meta:
        verbose_name_plural = "Guest Reservations"

    def __str__(self):
        return f"Reservation-ID: " + str(self.reservationID) + " / Confirmation #: " + str(
            self.confirmationKey) + " --- Guest: " + self.userID.first_name + " " + self.userID.last_name + " -- " + str(
                self.guests) + " guests for " + str(
                get_nights(self.checkInDate, self.checkOutDate)) + " nights -- " + str(
                    self.checkInDate) + " to " + str(self.checkOutDate)

    def save(self, *args, **kwargs):
        costs = (Stay_Costs.objects.filter(guests=self.guests).get()).price
        self.totalPrice = get_final_price(costs,self.checkInDate, self.checkOutDate, self.guests)
        self.confirmationKey = generate_confirmation_code(self.checkInDate, self.checkOutDate, self.guests, self.roomID)
        super(Reservations, self).save(*args, **kwargs)

#add class meta, and return strings. 