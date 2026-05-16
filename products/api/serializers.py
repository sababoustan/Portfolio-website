from rest_framework import serializers
from products.models import Product


class ProductDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "id",
            "title",
            "slug",
            "description",
            "price",
            "discount_price",
            "stock",
            "image",
            "category",
            "sku"
            ]