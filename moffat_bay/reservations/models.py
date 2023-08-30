from django.db import models

#stay costs model
class Stay_Costs(models.Model):
    guests = models.IntegerField(unique=True)
    price = models.DecimalField(decimal_places=2, max_digits=5)

    def __str__(self):
        return f"{self.guests} guests per night: ${self.price}"