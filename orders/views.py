from django.shortcuts import render
import uuid
import requests 
from django.views import View
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from cart.models import Cart
from accounts.models import Address
from .models import Order, OrderItem
from .services import verify_and_pay_order

MERCHANT = "zibal"   
ZIBAL_REQUEST = "https://gateway.zibal.ir/v1/request"
ZIBAL_VERIFY = "https://gateway.zibal.ir/v1/verify"
ZIBAL_STARTPAY = "https://gateway.zibal.ir/start/"


# Create your views here.
class ConfirmOrderView(View):
    model = Cart
    
    def post(self, request):
            selected_address_id = request.POST.get("selected_address")
            if not selected_address_id:
                return redirect("accounts:checkout")
            cart = Cart.objects.filter(user=request.user).first()
            items = cart.items.all()
            final_price = cart.get_final_price() 
            address = Address.objects.get(id=selected_address_id, 
                                          user=request.user)
            if address.city == "تهران":
                shipping_cost = 50000
            else:
                shipping_cost = 60000
                
            total_to_pay = final_price + shipping_cost
            context = {
                "address": address,
                "address_id": selected_address_id,
                "final_price": final_price,
                "shipping_cost": shipping_cost,
                "total_to_pay": total_to_pay,
                'items': items,
            }
            return render(request, "orders/preview_order.html", context)
        
        
class PaymentRequestView(View):
    def post(self, request):
        user = request.user
        address_id = request.POST.get("address")
        final_price = int(request.POST.get("final_price"))
        shipping_cost = int(request.POST.get("shipping_cost"))
        order_note = request.POST.get("order_note")
        total_price = final_price + shipping_cost
        cart = Cart.objects.filter(user=user).first()
        address = get_object_or_404(Address, id=address_id)
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
        callback_url = request.build_absolute_uri(
            reverse("orders:payment_verify")
        )
        payload = {
            "merchant": MERCHANT,
            "amount": total_price,
            "callbackUrl": callback_url,
            "description": "پرداخت تستی فروشگاه",
            "orderId": authority
        }
        response = requests.post(ZIBAL_REQUEST, json=payload).json()
        if response["result"] == 100:
            trackId = response["trackId"]
            return redirect(ZIBAL_STARTPAY + str(trackId))
        
        return render(request, "orders/payment_error.html",
                      {"message": response.get("message",
                                               "خطا در اتصال به درگاه")})
    
   
class PaymentVerifyView(View):
    def get(self, request):
        success = request.GET.get("success")
        track_id = request.GET.get("trackId")
        order_id = request.GET.get("orderId")

        order = Order.objects.filter(authority=order_id).first()
        if not order:
            return render(request, "orders/payment_error.html", {
                "message": "سفارش یافت نشد."
            })

        if success != "1":
            order.status = Order.status_order.Failed
            order.save()
            return render(request, "orders/payment_error.html", {
                "message": "پرداخت توسط کاربر لغو شد"
            })

        try:
            verify_and_pay_order(order, track_id)
        except Exception as e:
            return render(request, "orders/payment_error.html", {
                "message": str(e)
            })

        return render(request, "orders/payment_success.html", {
            "order": order
        })