from rest_framework.generics import ListCreateAPIView
from comments.api.serializers import CommentSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from comments.models import Comment
from django.shortcuts import get_object_or_404
from products.models import Product


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
            is_active=True,
        )