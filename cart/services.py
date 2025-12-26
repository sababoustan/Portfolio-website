from products.models import Product
from .models import CartItem


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