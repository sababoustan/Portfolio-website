from django.urls import path
from .views import (CartView, AddToCartView, RemoveItemView,
                    UpdateCartAjaxView, ApplyCouponView, wishlist_page,
                    WishlistToggleView)

app_name = 'cart'

urlpatterns = [
    path("", CartView.as_view(), name="cart_view"),

    path("add/<int:product_id>/", AddToCartView.as_view(), name="add_to_cart"),

    path("remove/<int:product_id>/", RemoveItemView.as_view(),
         name="remove_item"),

    path("update/", UpdateCartAjaxView.as_view(), name="update_cart_ajax"),

    path("apply-coupon/", ApplyCouponView.as_view(), name="apply_coupon"),

    path("wishlist/", wishlist_page, name="wishlist"),

    path("wishlist/toggle/<int:product_id>/", WishlistToggleView.as_view(),
         name="wishlist_toggle"),

]
