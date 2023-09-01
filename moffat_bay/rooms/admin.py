from django.contrib import admin
from .models import RoomChoices, Rooms

class RoomChoiceAdmin(admin.ModelAdmin):
    list_display = ('roomSize',)
    ordering = ['choiceID']
    readonly_fields = ('choiceID',)

    def has_add_permission(self, request):
        return True
    
    def has_delete_permission(self, request, obj=None):
        return True
    
    def has_change_permission(self, request, obj=None):
        return True

class RoomsAdmin(admin.ModelAdmin):
    ordering = ['roomID']
    readonly_fields = ('roomID',)

    def has_add_permission(self, request):
        return True
    
    def has_delete_permission(self, request, obj=None):
        return True
    
    def has_change_permission(self, request, obj=None):
        return True
    
admin.site.register(RoomChoices, RoomChoiceAdmin)
admin.site.register(Rooms, RoomsAdmin)