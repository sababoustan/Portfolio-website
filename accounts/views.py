from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm, RegisterForm, AddressForm
from django.contrib.auth.mixins import LoginRequiredMixin
from cart.models import Cart
from .models import User, Address


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
        
        return render(request, "accounts/shop-customer-login.html", {
            "login_form": LoginForm(),
            "register_form": RegisterForm(),
        })
        

class CheckoutView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'
    redirect_field_name = 'next'

    def get(self, request):
        address = Address.objects.filter(user=request.user)
        selected_id = request.GET.get("selected_address")
        form = AddressForm()
        cart = Cart.objects.filter(user=request.user).first()
        items = cart.items.all() if cart else []
        final_price = cart.get_final_price() if cart else 0
        if address:
            context = {
            'address_old': address,
            'selected_id': selected_id,
            'form': form,
            'items': items,
            'final_price': final_price,
            
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
            "address_form": form,
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
            return render(request, "orders/preview_order.html", context)
        
        
