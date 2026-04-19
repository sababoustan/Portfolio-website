from rest_framework.generics import (
                                RetrieveDestroyAPIView,
                                ListCreateAPIView,
                                ListAPIView
                                )
from rest_framework.permissions import (
                                IsAuthenticatedOrReadOnly,
                                BasePermission,
                                IsAuthenticated,
                                SAFE_METHODS,
                            )
from django.db.models import Q
from django.shortcuts import get_object_or_404
from products.api.serializers import ProductDetailSerializer, CommentSerializer
from products.models import Product
from comments.models import Comment
from orders.models import OrderItem
from cart.models import Wishlist


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_staff)
    

class ProductListAPI(ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer
    permission_classes = [IsAdminOrReadOnly]
    
    
class ProductDetailAPI(RetrieveDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer
    lookup_field = "slug"
    permission_classes = [IsAdminOrReadOnly]


class ProductCommentAPI(ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Comment.objects.filter(
            product__slug=self.kwargs["slug"],
            is_active=True,
            parent__isnull=True
        )

    def perform_create(self, serializer):
        product = get_object_or_404(Product, slug=self.kwargs["slug"])
        serializer.save(
            user=self.request.user,
            product=product,
            is_active=False
        )


class ProductSearchAPI(ListAPIView):
    serializer_class = ProductDetailSerializer

    def get_queryset(self):
        search = self.request.query_params.get('search', '').strip()
        qs = Product.objects.filter(is_active=True)
        if search:
            qs = qs.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search) |
                Q(slug__icontains=search)
            )
        return qs
    
    
class RecommendationProductAPI(ListAPIView):
    serializer_class = ProductDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        order_product_ids = OrderItem.objects.filter(
            order__user=self.request.user
        ).values_list('product_id', flat=True)

        wishlist_product_ids = Wishlist.objects.filter(
            user=self.request.user
        ).values_list('product_id', flat=True)
        
        product_ids = order_product_ids.union(wishlist_product_ids)
        category_id = Product.objects.filter(
            id__in=product_ids
            ).values_list('category_id', flat=True).distinct()

        return Product.objects.filter(
            category_id__in=category_id
            ).exclude(
                id__in=product_ids
                )[:10]

    