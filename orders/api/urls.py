from django.urls import path
from .views import (
    PaymentRequestAPI,
    PaymentVerifyAPI
)

app_name = "order_api"
urlpatterns = [

    path("payment-request/", PaymentRequestAPI.as_view(),
         name="payment_request"),

    path("payment-verify/", PaymentVerifyAPI.as_view(), name="payment_verify"),

]