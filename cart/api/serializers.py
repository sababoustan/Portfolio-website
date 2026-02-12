from rest_framework import serializers
from cart.models import Cart, CartItem, Wishlist


class CartItemSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CartItem
        fields = [
            "id",
            "product",
            "cart",
            "quantity",
            "product",
            "unit_price",
            "total_price",
            "added_at",
        ]
        

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_quantity = serializers.SerializerMethodField()
    discount_amount = serializers.SerializerMethodField()
    final_price = serializers.SerializerMethodField()
    coupon = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = [
            "id",
            "items",
            "coupon",
            "total_quantity",
            "final_price",
            "discount_amount",
            "created_at",
        ]
        
    def get_coupon(self, obj):
        return obj.coupon.code if obj.coupon else 0
        
    def get_total_quantity(self, obj):
        return obj.get_total_quantity()
    
    def get_discount_amount(self, obj):
        return obj.get_discount_amount()
    
    def get_final_price(self, obj):
        return obj.get_final_price()
        
    
class AddToCartInputSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    qty = serializers.IntegerField(min_value=1)
    
    
class CartActionSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    action = serializers.ChoiceField(
        choices=["increase", "decrease"]
    )
    
    
class CouponSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=50, allow_blank=False, 
                                 trim_whitespace=True)
    

class WishListSerializer(serializers.ModelSerializer):
    product = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = Wishlist
        fields = [
            "product",
            "added_at",
        ]