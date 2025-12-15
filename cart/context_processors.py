from .models import Cart, Wishlist


def cart_count(request):
    if not request.user.is_authenticated:
        return {"cart_count": 0}

    cart = Cart.objects.filter(
        user=request.user,
        status=Cart.Status.DRAFT
    ).first()

    return {
        "cart_count": cart.get_total_quantity() if cart else 0
    }


def wishlist_count(request):
    if request.user.is_authenticated:
        return {"wishlist_count": Wishlist.objects.filter(user=request.user)
                .count()}
    return {"wishlist_count": 0}
