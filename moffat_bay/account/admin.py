from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from account.models import Account
from django.contrib.auth.models import Group

@admin.action(description='Mark as inactive')
def mark_inactive(selc, request, queryset):
    queryset.update(is_active=False)


class AccountAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'phone')
    search_fields = ('email', 'first_name', 'last_name', 'phone')
    readonly_fields = ('id', 'date_joined', 'last_login')
    actions= [mark_inactive]
    ordering = ['email', 'is_active']

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

    
    


admin.site.register(Account, AccountAdmin)


