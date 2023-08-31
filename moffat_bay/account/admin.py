from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from account.models import Account, MailingList


#Custom user account actions for within the admin page: 
#We can add others if we choose
@admin.action(description='Mark as inactive')
def mark_inactive(selc, request, queryset):
    queryset.update(is_active=False)

#Custom Account Display for the Admin page. Records table will display
#email, first and last name, phone. can search by same fields
#restricts id, date_joined and last login to read-only
#adds custom account actions to admin page(as definied above)
#orders the user account table by email and if user is active. 
class AccountAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'phone')
    search_fields = ('email', 'first_name', 'last_name', 'phone')
    readonly_fields = ('id', 'date_joined', 'last_login')
    actions= [mark_inactive]
    ordering = ['email', 'is_active']

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


#registers the account model and account admin options with the admin page
admin.site.register(Account, AccountAdmin)
admin.site.register(MailingList)

admin.site.site_header = "Moffat-Bay Administration"
admin.site.site_title = "Moffat-Bay Administration"
admin.site.index_title = "Moffat-Bay Administration"