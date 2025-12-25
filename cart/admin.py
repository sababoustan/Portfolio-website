from django.contrib import admin
from .models import Cart, CartItem, Coupon, Wishlist


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
    
    
admin.site.register(Cart, CartAdmin)
admin.site.register(Coupon)        
admin.site.register(Wishlist)
    
    
    
