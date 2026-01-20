from rest_framework.generics import (
                                RetrieveDestroyAPIView, 
                                ListCreateAPIView, 
                                ListAPIView
                                )
from rest_framework.permissions import (
                                IsAuthenticatedOrReadOnly,
                                BasePermission,
                                SAFE_METHODS,
                            )
from django.db.models import Q
from django.shortcuts import get_object_or_404
from products.api.serializers import ProductDetailSerializer, CommentSerializer
from products.models import Product
from comments.models import Comment


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

    
    