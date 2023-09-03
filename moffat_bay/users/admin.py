# src/users/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from .models import CustomUser, MailingList

#Custom user account actions for within the admin page: 
#We can add others if we choose
@admin.action(description='Mark as inactive')
def mark_inactive(selc, request, queryset):
    queryset.update(is_active=False)

#Custom Account Display for the Admin page. 
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'is_staff', 'is_active',)
    list_filter = ('email', 'is_staff', 'is_active',)
    fieldsets = (
        ('User Account Information', {'fields': ('email', 'password')}),
        ('Personal Information', {'fields': ('first_name', 'last_name', 'street', 'city', 'state', 'zip', 'phone')}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser', 'is_active')}),
    
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'first_name', 'last_name', 'street', 'city', 'state', 'zip', 'phone','is_staff', 'is_superuser', 'is_active')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)

    def has_add_permission(self, request):
       return True
    
    def has_delete_permission(self, request, obj=None):
        return True
    
    def has_change_permission(self, request, obj=None):
        return True


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(MailingList)


#change admin site titles/headers
admin.site.site_header = "Moffat-Bay Administration"
admin.site.site_title = "Moffat-Bay Administration"
admin.site.index_title = "Database Administration"

#remove groups from admin site (groups are defaulted with built in users, we are using custom user models)
admin.site.unregister(Group)
