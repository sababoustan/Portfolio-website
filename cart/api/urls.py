from django.urls import path
from cart.api.views import (
    CartAPI,
    CartItemAPI,
    AddToCartAPI,
    UpdateCartAPI,
    CouponAPI,
    WishlistAPI,
    WishlistToggleAPIView
)

app_name = "cart_api"
urlpatterns = [
    path("cart/", CartAPI.as_view(), name="cart"),
    path("cartitem/<int:item_id>/", CartItemAPI.as_view(), name="cartitem"),
    path("cart/add/", AddToCartAPI.as_view(), name="add-to-cart"),
    path("cart/update/", UpdateCartAPI.as_view(), name="cart-update"),
    path("cart/coupon/", CouponAPI.as_view(), name="coupon"),
    path("wishlist/", WishlistAPI.as_view(), name="wishlist"),
    path("wishlist/toggle/<int:product_id>/", WishlistToggleAPIView.as_view(), name="wishlist"),
]