from django.shortcuts import render
from django.views import View
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import redirect, get_object_or_404
from .models import Cart, CartItem, Coupon, Wishlist, Product
from django.db.models import Count


# Create your views here.
class CartMixin:
    def get_cart(self):
        request = self.request

        if request.user.is_authenticated:
            cart = Cart.objects.filter(
                user=request.user,
                status=Cart.Status.DRAFT
            ).first()

            if not cart:
                cart = Cart.objects.create(
                    user=request.user,
                    status=Cart.Status.DRAFT
                )

            return cart

        if not request.session.session_key:
            request.session.create()

        cart = Cart.objects.filter(
            session_id=request.session.session_key,
            status=Cart.Status.DRAFT
        ).first()

        if not cart:
            cart = Cart.objects.create(
                session_id=request.session.session_key,
                status=Cart.Status.DRAFT
            )

        return cart


class CartView(CartMixin, View):
    template_name = "cart/shop-cart.html"
    
    def get(self, request):
        cart = self.get_cart()
        context = {
            'cart': cart,
            'items': cart.items.all(),
            'total_price': cart.total_price,
            'discount': cart.get_discount_amount(),
            'final_price': cart.get_final_price()
        }
        return render(request, self.template_name, context)
    
    
class AddToCartView(CartMixin, View):
    def post(self, request, product_id):
        cart = self.get_cart()
        product = Product.objects.get(id=product_id)
        qty = int(request.POST.get("quantity", 1))
        item = cart.items.filter(product=product).first()
        if item:
            new_qty = item.quantity + qty

            if new_qty > product.stock:
                return JsonResponse({
                    "error": "این تعداد بیشتر از موجودی محصول است"
                }, status=400)

            item.quantity = new_qty
            item.save()
        else:
            if qty > product.stock:
                return JsonResponse({
                    "error": "این تعداد موجود نیست"
                }, status=400)
            CartItem.objects.create(
                cart=cart,
                product=product,
                unit_price=product.price,
                quantity=qty
            )
        cart.refresh_from_db()
        cart.update_total_price()
        cart_count = cart.items.aggregate(total=Count("id"))["total"]

        return JsonResponse({
            "status": "added",
            "cart_count": cart_count
        })
    

class RemoveItemView(CartMixin, View):
    def post(self, product_id):
        cart = self.get_cart()
        product = Product.objects.get(id=product_id)
        item = cart.items.filter(product=product).first()
        if not item:
            return redirect("cart:cart_view")
        if item.quantity > 1:
            item.quantity -= 1
            item.save()
        else:
            item.delete()
        cart.update_total_price()
        return redirect("cart:cart_view")
   
    
class UpdateCartAjaxView(CartMixin, View):
    def post(self, request):
        product_id = request.POST.get("product_id")
        action = request.POST.get("action")

        cart = self.get_cart()
        product = get_object_or_404(Product, id=product_id)

        item = cart.items.filter(product=product).first()

        if not item:
            return JsonResponse({"error": "Item not found"}, status=404)
        
        removed = False 
        
        if action == "increase":
            if item.quantity < item.product.stock:
                item.quantity += 1
                item.save()
            else:
                return JsonResponse({
                    "error": "max_stock",
                    "message": "حداکثر موجودی محصول همین تعداد است"
                })

        elif action == "decrease":
            if item.quantity > 1:
                item.quantity -= 1
                item.save()
            else:
                item.delete()
                removed = True 

        cart.update_total_price()

        return JsonResponse({
            "removed": removed,
            "quantity": item.quantity if not removed else 0,
            "item_total": item.total_price if not removed else 0,
            "cart_total": cart.total_price,
            "discount": cart.get_discount_amount(),
            "final_total": cart.get_final_price(),
            "cart_count": cart.get_total_quantity(),
        })
    
          
class ApplyCouponView(CartMixin, View):
    def post(self, request):
        cart = self.get_cart()
        code = request.POST.get("code")
        if not code:
            messages.error(request, "کد تخفیف وارد نشده است.")
            return redirect("cart:cart_view")
        coupon = Coupon.objects.filter(code=code).first()
        if not coupon:
            messages.error(request, "کد تخفیف اشتباه است.")
            return redirect("cart:cart_view")
        cart.coupon = coupon
        cart.save()
        discount = cart.get_discount_amount()
        if discount == 0:
            messages.error(request, "شرایط اعمال کد تخفیف رعایت نشده است.")
            cart.coupon = None
            cart.save()
        else:
            messages.success(request, "کد تخفیف با موفقیت اعمال شد.")
        
        return redirect("cart:cart_view")
    
    
class WishlistListView(View):
    def get(self, request):
        items = Wishlist.objects.filter(user=request.user)
        return render(request, "cart/shop-wishlist.html", {"items": items})
    
    
class WishlistToggleView(View):
    def post(self, request, product_id):
        if not request.user.is_authenticated:
            return JsonResponse({
                "status": "error",
                "message": "login_required"
            }, status=401)

        product = get_object_or_404(Product, id=product_id)

        wishlist_item = Wishlist.objects.filter(
            user=request.user,
            product=product
        ).first()

        if wishlist_item:
            wishlist_item.delete()
            status = "removed"
        else:
            Wishlist.objects.create(
                user=request.user,
                product=product
            )
            status = "added"
        wishlist_count = Wishlist.objects.filter(user=request.user).count()

        return JsonResponse({
            "status": status,
            "wishlist_count": wishlist_count
        })