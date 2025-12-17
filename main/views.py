from django.views.generic import ListView
from products.models import Product
from cart.models import Wishlist
import math


# Create your views here.
class HomeView(ListView):
    model = Product
    template_name = "main/index.html"
    context_object_name = "products"
    page_size = 8

    def get_queryset(self):
        return Product.objects.filter(
            is_active=True
        ).order_by("-created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        queryset = self.get_queryset()

        # --- pagination ---
        try:
            page_number = int(self.request.GET.get("page", 1))
        except ValueError:
            page_number = 1

        if page_number < 1:
            page_number = 1

        total_items = queryset.count()
        total_pages = math.ceil(total_items / self.page_size)

        if total_pages > 0 and page_number > total_pages:
            page_number = total_pages

        offset = (page_number - 1) * self.page_size
        end = offset + self.page_size
        page_objects = queryset[offset:end]

        context["products"] = page_objects
        context["current_page"] = page_number
        context["total_pages"] = total_pages
        context["has_previous"] = page_number > 1
        context["has_next"] = page_number < total_pages

        # --- wishlist ---
        if self.request.user.is_authenticated:
            context["wishlist_ids"] = Wishlist.objects.filter(
                user=self.request.user
            ).values_list("product_id", flat=True)
        else:
            context["wishlist_ids"] = []

        return context
