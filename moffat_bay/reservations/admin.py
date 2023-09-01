from django.contrib import admin
from .models import Stay_Costs

#admin classes to handle how they appear on admin page
class CostAdmin(admin.ModelAdmin):

    list_display = ('guests', 'price')
    readonly_fields = ('guests',)
    ordering = ['guests']

    def has_add_permission(self, request):
        return True
    
    def has_delete_permission(self, request, obj=None):
        return True
    
    def has_change_permission(self, request, obj=None):
        return True


# Register models for admin page here.
admin.site.register(Stay_Costs, CostAdmin)

