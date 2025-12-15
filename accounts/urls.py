from django.urls import path
from .views import (LoginView, RegisterView, LogoutView, CheckoutView,
                    ConfirmOrderView, PaymentVerifyView,
                    PaymentRequestView)

app_name = 'accounts'

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("checkout/", CheckoutView.as_view(), name="checkout"),
    path("register/", RegisterView.as_view(), name="register"),
    path("confirmorder/", ConfirmOrderView.as_view(), name="confirm_order"),
    path("paymentverify/", PaymentRequestView.as_view(), 
         name="payment_request"),
    path("payment-verify/", PaymentVerifyView.as_view(), 
         name="payment_verify"),


]