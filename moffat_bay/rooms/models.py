from django.db import models

#room sizes model - for room size choices
class RoomChoices(models.Model):
    choiceID = models.IntegerField(primary_key=True, auto_created=True)
    roomSize = models.CharField(max_length=50, null=False, unique=True)
    
    def __str__(name) -> str:
        return name.roomSize
    
    
    class Meta:
        verbose_name_plural = "Room Size Choices"
   
    
#rooms model - modeling for how many rooms the lodge has and of what type
class Rooms(models.Model):
    roomID = models.IntegerField(primary_key=True, auto_created=True)
    size = models.ForeignKey(RoomChoices, to_field="roomSize", on_delete=models.CASCADE)
    class Meta:
        verbose_name_plural = "Lodge Rooms"
    
    def __str__(name) -> str:
        return "Room # " + str(name.roomID) + " - " + str(name.size)
    
