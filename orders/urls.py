from django.urls import path
from .views import PaymentRequestView, PaymentVerifyView

app_name = 'orders'

urlpatterns = [
    path("paymentverify/", PaymentRequestView.as_view(), 
         name="payment_request"),
    path("payment-verify/", PaymentVerifyView.as_view(), 
         name="payment_verify"),
]
