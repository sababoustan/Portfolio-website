from django.views.generic import TemplateView
from products.models import Product
from cart.models import Wishlist


# Create your views here.
class HomeView(TemplateView):
    template_name = "main/index.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["products"] = Product.objects.filter(
            is_active=True
        ).order_by("-created_at")

        if self.request.user.is_authenticated:
            context["wishlist_ids"] = Wishlist.objects.filter(
                user=self.request.user
            ).values_list("product_id", flat=True)
        else:
            context["wishlist_ids"] = []
        return context