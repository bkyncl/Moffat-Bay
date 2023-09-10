# Mark Witt / Brittany Kyncl
# CSD-440: Capstone Project
# Moffat-Bay Lodge - Bravo Team


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
    list_display = ('email', 'first_name', 'last_name', 'is_active',)#
    list_filter = ('first_name', 'last_name', 'email')
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
    search_fields = ('email', 'phone', 'first_name', 'last_name')
    search_help_text = ("Search by:  Email, Phone #, First Name, or Last Name.")
    ordering = ('first_name', 'last_name', 'email', 'is_active')
    actions=[mark_inactive,]

    def has_add_permission(self, request):
       return True
    
    def has_delete_permission(self, request, obj=None):
        return True
    
    def has_change_permission(self, request, obj=None):
        return True
    def has_recent_actions(self, request):
        return False
class MailingListAdmin(admin.ModelAdmin):
    model = MailingList
    list_display = ('email',)
    search_fields = ('email',)
    search_help_text = ("Search by Email Address")
    ordering = ('email',)

    def has_add_permission(self, request):
       return False
    
    def has_delete_permission(self, request, obj=None):
        return True
    
    def has_change_permission(self, request, obj=None):
        return False
    def has_recent_actions(self, request):
        return False
    
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(MailingList, MailingListAdmin)


#change admin site titles/headers
admin.site.site_header = "Moffat-Bay Administration"
admin.site.site_title = "Moffat-Bay Administration"
admin.site.index_title = "Database Administration"

#remove groups from admin site (groups are defaulted with built in users, we are using custom user models)
admin.site.unregister(Group)

