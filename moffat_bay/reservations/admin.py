# Mark Witt / Brittany Kyncl
# CSD-440: Capstone Project
# Moffat-Bay Lodge - Bravo Team

from django.contrib import admin
from .models import Stay_Costs, Reservations
from django.http import HttpResponseRedirect
from django.urls import reverse

#custom admin actions

def update_prices(modeladmin, request, queryset):
    product_ids = queryset.values_list('id', flat=True)
    return HttpResponseRedirect(reverse('price_update')+ '?id=' + ','.join(str(p) for p in product_ids))

def change_prices(modeladmin, request, queryset):
    product_ids = queryset.values_list('id', flat=True)
    return HttpResponseRedirect(reverse('price_change')+ '?id=' + ','.join(str(p) for p in product_ids))

update_prices.short_description = "Update Prices: By Percentage"
change_prices.short_description = "Update Prices: Direct $ Entry"

#admin classes to handle how they appear on admin page
class CostAdmin(admin.ModelAdmin):
    list_display = ('guests', 'price')
    readonly_fields = ('guests',)
    ordering = ['guests']
    actions = [update_prices, change_prices]

    def has_add_permission(self, request):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
    def has_recent_actions(self, request):
        return False
    
#add admin class for reservations model
class ReservationsAdmin(admin.ModelAdmin):
    model = Reservations
    readonly_fields = ('reservationID', 'confirmationKey', 'userID', 'totalPrice', 'roomID')
    ordering = ('checkInDate', 'checkOutDate')
    search_fields = ('reservationID', 'confirmationKey', 'checkInDate', 'checkOutDate')
    fieldsets = (
        ('Reservation', {'fields': ('reservationID', 'confirmationKey')}),
        ('Reservation Details', {'fields' : ('checkInDate', 'checkOutDate', 'roomID', 'guests', 'totalPrice')}),
        ('User Details - click to see user account', {'fields': ('userID',)}),
    )
    list_filter = ('checkInDate', 'checkOutDate', 'userID')
    search_help_text = ("Search by:  Reservation #, Confirmation #, Check-in Date (YYYY-MM-DD), or Check-out Date (YYYY-MM-DD).")
    

    def has_add_permission(self, request):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return True
    
    def has_change_permission(self, request, obj=None):
        return True
    def has_recent_actions(self, request):
        return True


# Register models for admin page here.
admin.site.register(Stay_Costs, CostAdmin)
admin.site.register(Reservations, ReservationsAdmin)



