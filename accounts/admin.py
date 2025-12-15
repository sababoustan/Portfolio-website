from django.contrib import admin
from .models import User, Address
# Register your models here.


class AddressInline(admin.TabularInline):
    search_fields = ["user__username", "city", "street_address"]
    model = Address
    
    
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'date_joined']
    search_fields = ['username', 'email']
    list_filter = ['date_joined']
    sortable_by = ['date_joined']
    fieldsets = [
        ("اطلاعات کاربر", {'fields': ('username', 'email')}),
        ("سیستمی", {'fields': ('date_joined',)})
      ]

    readonly_fields = ['date_joined']
    inlines = [AddressInline]
