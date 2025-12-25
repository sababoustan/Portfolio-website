from django.contrib import admin
from .models import Order, OrderItem


# Register your models here.
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ["product", "quantity", "total_price"]
    
    
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "status", "created_at", "authority", 
                    "total_price"]
    list_filter = ["status", "created_at"]
    search_fields = ["user__username", "authority"]
    readonly_fields = ["total_price"]
    inlines = [OrderItemInline]
    
    def has_add_permission(self, request):
        return False