from rest_framework import serializers
from orders.models import Order


class PaymentRequestSerializer(serializers.Serializer):
    address = serializers.IntegerField()
    final_price = serializers.IntegerField()
    shipping_cost = serializers.IntegerField()
    order_note = serializers.CharField(required=False, allow_blank=True)
    callback_url = serializers.URLField()


class OrderSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(source='get_status_display', 
                                           read_only=True)
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    address = serializers.PrimaryKeyRelatedField(read_only=True)
    cart = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Order
        fields = [
            'id',
            'user',
            'cart',
            'address',
            'status',
            'status_display',
            'created_at',
            'payment_tracking_code',
            'authority',
            'total_price',
            'order_note',
        ]
        read_only_fields = fields