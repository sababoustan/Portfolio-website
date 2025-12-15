from django.contrib import admin
from .models import Cart, CartItem, Coupon, Wishlist, Order, OrderItem


# Register your models here.
class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    readonly_fields = ['unit_price', 'total_price']


class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'status', 'total_price', 'discount_amount',
                    'final_price', 'created_at']
    search_fields = ["user__username"]
    readonly_fields = ['total_price']
    inlines = [CartItemInline]
    
    def discount_amount(self, obj):
        return obj.get_discount_amount()
    discount_amount.short_description = "مقدار تخفیف"

    def final_price(self, obj):
        return obj.get_final_price()
    final_price.short_description = "مبلغ نهایی"
    

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
    
    
admin.site.register(Cart, CartAdmin)
admin.site.register(Coupon)        
admin.site.register(Wishlist)
    
    
    
