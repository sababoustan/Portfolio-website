from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.urls import reverse
from cart.models import Cart
from accounts.models import Address
from .models import Order
from .services import verify_and_pay_order, create_order, request_zibal_payment

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
        address = get_object_or_404(Address, id=address_id, user=user)        
        order = create_order(
            user=user,
            cart=cart,
            address=address,
            total_price=total_price, 
            order_note=order_note
        )
        callback_url = request.build_absolute_uri(
            reverse("orders:payment_verify")
        )
        response = request_zibal_payment(order, callback_url)
        if response.get("result") == 100:
            return redirect(ZIBAL_STARTPAY + str(response["trackId"]))
        
        return render(request, 
                      "orders/payment_error.html",
                      {"message": response.get("message","خطا در اتصال به درگاه")}
                      )
    
   
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