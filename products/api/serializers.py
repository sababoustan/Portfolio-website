from rest_framework import serializers
from products.models import Product
from comments.models import Comment


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
            "discount_price"
            ]
        
        
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            "id", 
            "user", 
            "body", 
            "created_at"
            ]