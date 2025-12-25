from django.db import transaction
from django.core.exceptions import ValidationError
from django.conf import settings
import uuid
import requests
from .models import Order
from .models import Order, OrderItem

MERCHANT = "zibal"
ZIBAL_REQUEST = "https://gateway.zibal.ir/v1/request"
ZIBAL_VERIFY = "https://gateway.zibal.ir/v1/verify"
ZIBAL_STARTPAY = "https://gateway.zibal.ir/start/"


def create_order(user, cart, address, total_price, order_note):
    authority = str(uuid.uuid4())
    order = Order.objects.create(
            user=user,
            cart=cart,
            address=address,
            total_price=total_price, 
            status=Order.status_order.PendingPayment,
            authority=authority,
            order_note=order_note
        )
    for item in cart.items.all():
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            total_price=item.total_price
        )
    return order


def request_zibal_payment(order, callback_url):
    payload = {
            "merchant": MERCHANT,
            "amount": int(order.total_price),
            "callbackUrl": callback_url,
            "description": "پرداخت تستی فروشگاه",
            "orderId": order.authority
        }
    return requests.post(ZIBAL_REQUEST, json=payload).json()

def verify_and_pay_order(order, track_id):
    if order.status == Order.status_order.Paid:
        return order

    payload = {
        "merchant": MERCHANT,
        "trackId": track_id,
    }

    response = requests.post(ZIBAL_VERIFY, json=payload).json()

    if response.get("result") not in (100, 201):
        raise ValidationError(
            response.get("message", "پرداخت ناموفق بود")
        )

    ref_number = response.get("refNumber")
    if not ref_number:
        if settings.DEBUG:
            ref_number = f"TEST-{track_id}"
        else:
            raise ValidationError("کد پیگیری پرداخت دریافت نشد")

    with transaction.atomic():
        order_items = order.items.select_related("product")

        for item in order_items:
            if item.product.stock < item.quantity:
                raise ValidationError(
                    f"موجودی محصول «{item.product.title}» کافی نیست"
                )

        for item in order_items:
            item.product.stock -= item.quantity
            item.product.save()

        order.status = Order.status_order.Paid
        order.ref_id = ref_number
        order.save()

        order.cart.items.all().delete()

    return order


