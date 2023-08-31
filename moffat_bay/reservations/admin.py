from django.contrib import admin
from .models import Stay_Costs

class CostAdmin(admin.ModelAdmin):

    list_display = ('guests', 'price')
    readonly_fields = ('guests',)
    ordering = ['guests']

    def has_add_permission(self, request):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False
    
    def has_change_permission(self, request, obj=None):
        return True


# Register models for admin page here.
admin.site.register(Stay_Costs, CostAdmin)
