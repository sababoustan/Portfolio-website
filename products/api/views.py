from rest_framework.generics import (
                                RetrieveDestroyAPIView,
                                ListCreateAPIView,
                                ListAPIView
                                )
from rest_framework.permissions import (
                                BasePermission,
                                IsAuthenticated,
                                SAFE_METHODS,
                                AllowAny
                            )
from django.db.models import Q
from rest_framework.response import Response
from products.api.serializers import ProductDetailSerializer
from products.models import Product
from orders.models import OrderItem
from cart.models import Wishlist
from django.core.cache import cache
from django.conf import settings


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_staff)


class ProductListAPI(ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        cache_key = "product_list"
        products = cache.get(cache_key)
        if products is None:
            queryset = self.get_queryset()
            serializer = self.serializer_class(queryset, many=True)
            products = serializer.data
            cache.set(cache_key, products, timeout=settings.CACHE_TTL)

        return Response(products)

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        cache.delete("product_list")
        return response


class ProductDetailAPI(RetrieveDestroyAPIView):
    queryset = Product.objects.all()
    lookup_field = "slug"
    serializer_class = ProductDetailSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request, *args, **kwargs):
        slug = self.kwargs.get('slug')
        cache_key = f"detail_product_{slug}"
        product = cache.get(cache_key)
        if product is None:
            product_obj = self.get_object()
            serializer = self.serializer_class(product_obj)
            product = serializer.data
            cache.set(cache_key, product, timeout=settings.CACHE_TTL)

        return Response(product)


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