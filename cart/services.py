from django.db import transaction
from django.shortcuts import get_object_or_404
from products.models import Product
from .models import CartItem, Coupon


class AddToCartService:
    
    @staticmethod
    def add(cart, product_id, qty):
        product = Product.objects.get(id=product_id)
        item = cart.items.filter(product=product).first()
        if item:
            new_qty = item.quantity + qty
            if new_qty > product.stock:
                raise ValueError("این تعداد بیشتر از موجودی محصول است")

            item.quantity = new_qty
            item.save()
        else:
            if qty > product.stock:
                raise ValueError("این تعداد موجود نیست")
            CartItem.objects.create(
                cart=cart,
                product=product,
                unit_price=product.price,
                quantity=qty
            )
            cart.refresh_from_db()
            cart.update_total_price()
            return cart.items.count()
        

class UpdateCartItemService:

    @staticmethod
    @transaction.atomic
    def update(product_id, cart, action):
        product = get_object_or_404(Product, id=product_id)
        item = cart.items.filter(product=product).first()
        if not item:
            raise ValueError("ITEM_NOT_FOUND")
        
        removed = False 
        
        if action == "increase":
            if item.quantity < item.product.stock:
                raise ValueError("MAX_STOCK")
            item.quantity += 1
            item.save()

        elif action == "decrease":
            if item.quantity > 1:
                item.quantity -= 1
                item.save()
            else:
                item.delete()
                removed = True 
        else:
            raise ValueError("INVALID_ACTION")

        cart.update_total_price()
        return {
            "removed": removed,
            "quantity": item.quantity if not removed else 0,
            "item_total": item.total_price if not removed else 0,
            "cart_total": cart.total_price,
            "discount": cart.get_discount_amount(),
            "final_total": cart.get_final_price(),
            "cart_count": cart.get_total_quantity(),
        }
        
        
class ApplyCouponService:
    
    @staticmethod
    def apply(code, cart):
        if not code:
            raise ValueError("EMPTY_CODE")
        coupon = Coupon.objects.filter(code=code).first()
        if not coupon:
            raise ValueError("INVALID_CODE")
        cart.coupon = coupon
        cart.save()
        discount = cart.get_discount_amount()
        discount = cart.get_discount_amount()
        if discount == 0:
            cart.coupon = None
            cart.save()
            raise ValueError("CONDITION_NOT_MET")
        return discount
