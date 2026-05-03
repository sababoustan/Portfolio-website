from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from cart.models import Cart
from accounts.models import Address
from orders.api.serializers import PaymentRequestSerializer, OrderSerializer
from rest_framework import status
from rest_framework.permissions import (
    IsAuthenticated)
from rest_framework.response import Response
from orders.services import (create_order, request_zibal_payment,
                             verify_and_pay_order)
from orders.models import Order

ZIBAL_STARTPAY = "https://gateway.zibal.ir/start/"
MERCHANT = "zibal"
ZIBAL_REQUEST = "https://gateway.zibal.ir/v1/request"
ZIBAL_VERIFY = "https://gateway.zibal.ir/v1/verify"


class PaymentRequestAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        serializer = PaymentRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        address_id = serializer.validated_data["address"]
        order_note = serializer.validated_data.get("order_note")
        callback_url = serializer.validated_data["callback_url"]
        cart = Cart.objects.filter(user=user, status=Cart.Status.DRAFT).first()
        if not cart.items.exists():
            return Response(
                {"detail": "Cart is empty"},
                status=status.HTTP_400_BAD_REQUEST
            )
        address = get_object_or_404(Address, id=address_id, user=user)
        final_price = cart.get_final_price()
        shipping_cost = 50000 if address.city == "تهران" else 60000
        total_price = final_price + shipping_cost
        order = create_order(
            user=user,
            cart=cart,
            address=address,
            total_price=total_price,
            order_note=order_note
        )
        response = request_zibal_payment(order, callback_url)
        if response.get("result") == 100:
            payment_url = ZIBAL_STARTPAY + str(response["trackId"])
            return Response({"payment_url": payment_url},
                            status=status.HTTP_200_OK)
        else:
            return Response(
                {"detail": "Error requesting payment from Zibal",
                 "message": response.get("message")},
                status=status.HTTP_400_BAD_REQUEST
            )


class PaymentVerifyAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        success = request.GET.get("success")
        track_id = request.GET.get("trackId")
        order_id = request.GET.get("orderId")

        order = get_object_or_404(Order, authority=order_id)
        if success != "1":
            order.status = Order.status_order.Failed
            order.save()
            return Response(
                {
                    "status": "failed",
                    "message": "Payment canceled by user."
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            order = verify_and_pay_order(order, track_id)
            ref_number = order.ref_id
        except Exception as e:
            return Response(
                {
                    "status": "failed",
                    "message": str(e)
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(
            {
                "status": "success",
                "message": "Payment verified successfully.",
                "ref_number": ref_number,
                "order_id": order.id,
                "track_id": track_id,
                "order_details": OrderSerializer(order).data,
             },
            status=status.HTTP_200_OK
        )