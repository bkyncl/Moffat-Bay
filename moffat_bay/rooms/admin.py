# Mark Witt / Brittany Kyncl
# CSD-440: Capstone Project
# Moffat-Bay Lodge - Bravo Team

from django.contrib import admin
from .models import RoomChoices, Rooms

class RoomChoiceAdmin(admin.ModelAdmin):
    list_display = ('roomSize',)
    ordering = ['choiceID']
    readonly_fields = ('choiceID',)

    def has_add_permission(self, request):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False

class RoomsAdmin(admin.ModelAdmin):
    ordering = ['roomID']
    readonly_fields = ('roomID',)

    def has_add_permission(self, request):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
    
admin.site.register(RoomChoices, RoomChoiceAdmin)
admin.site.register(Rooms, RoomsAdmin)