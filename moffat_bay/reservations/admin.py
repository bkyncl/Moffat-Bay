from django.contrib import admin
from .models import Stay_Costs

class CostAdmin(admin.ModelAdmin):
    list_display = ('guests', 'price')
    search_fields = ('guests', 'price')
    readonly_fields = ('guests',)
    ordering = ['guests']

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

# Register your models here.
admin.site.register(Stay_Costs, CostAdmin)