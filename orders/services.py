from django.db import transaction
from django.core.exceptions import ValidationError
from django.conf import settings
import requests
from .models import Order

MERCHANT = "zibal"
ZIBAL_REQUEST = "https://gateway.zibal.ir/v1/request"
ZIBAL_VERIFY = "https://gateway.zibal.ir/v1/verify"
ZIBAL_STARTPAY = "https://gateway.zibal.ir/start/"


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


