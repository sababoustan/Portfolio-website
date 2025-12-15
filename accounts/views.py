from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
import uuid
from django.contrib import messages
from django.db import transaction
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm, RegisterForm, AddressForm
from django.contrib.auth.mixins import LoginRequiredMixin
from cart.models import Cart, Order, OrderItem
from .models import User, Address
import requests 

MERCHANT = "zibal"   
ZIBAL_REQUEST = "https://gateway.zibal.ir/v1/request"
ZIBAL_VERIFY = "https://gateway.zibal.ir/v1/verify"
ZIBAL_STARTPAY = "https://gateway.zibal.ir/start/"


class LoginView(View):

    def get(self, request):
        return render(request, "accounts/shop-customer-login.html", {
            "login_form": LoginForm(),
            "register_form": RegisterForm(),
        })

    def post(self, request):
        login_form = LoginForm(request.POST)

        if login_form.is_valid():
            username_or_email = login_form.cleaned_data["username_or_email"]
            password = login_form.cleaned_data["password"]

            if "@" in username_or_email:
                try:
                    user_obj = User.objects.get(email=username_or_email)
                    username = user_obj.username
                except User.DoesNotExist:
                    username = None
            else:
                username = username_or_email

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                next_url = request.GET.get("next")
                if next_url:
                    return redirect(next_url)
                return redirect("main:home")

            else:
                messages.error(request, "نام کاربری یا رمز اشتباه است")

        return render(request, "accounts/shop-customer-login.html", {
            "login_form": login_form,
            "register_form": RegisterForm(),
        })


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("main:home")
        
        
class RegisterView(View):
    def get(self, request):
        return render(request, "accounts/shop-customer-login.html", {
            "login_form": LoginForm(),
            "register_form": RegisterForm(),
        })
    
    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user = register_form.save(commit=False)
            user.set_password(register_form.cleaned_data["password"])
            user.save()
            messages.success(request, "ثبت نام با موفقطیت  انجام شد")
            return redirect("main:home")
        else:
            register_form = RegisterForm()
        print("VALID:", register_form.is_valid())
        print(register_form.errors)
        return render(request, "accounts/shop-customer-login.html", {
            "login_form": LoginForm(),
            "register_form": RegisterForm(),
        })
        

class CheckoutView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'
    redirect_field_name = 'next'
    model = Address

    def get(self, request):
        address = Address.objects.filter(user=request.user)
        selected_id = request.GET.get("selected_address")
        form = AddressForm()
        cart = Cart.objects.filter(user=request.user).first()
        if cart:
            items = cart.items.all()
        else:
            items = []
        if address:
            context = {
            'address_old': address,
            'selected_id': selected_id,
            'form': form,
            'items': items,
            'final_price': cart.get_final_price(),
            
            }
            return render(request, "accounts/address_checkout.html",context)
        
        address_form = AddressForm()
        return render(request, "accounts/address_checkout.html", 
                      {"form": address_form}
                      )

    def post(self, request):
        form = AddressForm(request.POST)
        if form .is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            messages.success(request, "آدرس شما با موفقیت ذخیره شد.")
            return redirect(f"{reverse('accounts:checkout')}?selected_address={address.id}")

        return render(request, "accounts/address_checkout.html", {
            "address_form": form 
        })
      
        
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
            return render(request, "accounts/preview_order.html", context)
        
        
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
            reverse("accounts:payment_verify")
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
        
        return render(request, "payment_error.html",
                      {"message": response.get("message",
                                               "خطا در اتصال به درگاه")})
    
            
class PaymentVerifyView(View):
    def get(self, request):
        success = request.GET.get("success")
        trackId = request.GET.get("trackId")
        order_id = request.GET.get("orderId")

        order = Order.objects.filter(authority=order_id).first()
        if not order:
            return render(request, "accounts/payment_error.html", {
                "message": "سفارش یافت نشد."
            })

        if success != "1":
            order.status = Order.status_order.Failed
            order.save()
            return render(request, "accounts/payment_error.html", {
                "message": "پرداخت توسط کاربر لغو شد"
            })

        payload = {
            "merchant": MERCHANT,
            "trackId": trackId,
        }
        response = requests.post(ZIBAL_VERIFY, json=payload).json()

        if response.get("result") != 100:
            order.status = Order.status_order.Failed
            order.save()
            return render(request, "accounts/payment_error.html", {
                "message": response.get("message", "پرداخت ناموفق بود")
            })

        try:
            with transaction.atomic():
                order_items = order.items.select_related("product")

                for item in order_items:
                    if item.product.stock < item.quantity:
                        raise Exception(
                            f"موجودی محصول «{item.product.title}» کافی نیست"
                        )

                for item in order_items:
                    item.product.stock -= item.quantity
                    item.product.save()

                ref_number = response.get("refNumber")
                if not ref_number:
                    raise Exception("کد پیگیری پرداخت دریافت نشد")

                order.status = Order.status_order.Paid
                order.ref_id = ref_number
                order.save()

                order.cart.items.all().delete()
            print("ZIBAL VERIFY RESPONSE:", response)
        except Exception as e:
            return render(request, "accounts/payment_error.html", {
                "message": str(e)
            })

        return render(request, "accounts/payment_success.html", {
            "order": order
        })

            
            
        
