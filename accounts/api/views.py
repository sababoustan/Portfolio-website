from rest_framework.generics import (
                                CreateAPIView,
                                ListAPIView,
                                DestroyAPIView,
                                RetrieveUpdateDestroyAPIView
                            )
from rest_framework.views import APIView
from rest_framework.exceptions import PermissionDenied
from django.contrib.auth import login, logout, get_user_model
from rest_framework.permissions import (
    IsAuthenticated, IsAdminUser)
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
from accounts.api.serializers import (
    UserSerializer, LoginSerializer, RegisterSerializer,
    ChangePasswordSerializer, AddressSerializer)
from accounts.models import Address
from cart.api.serializers import CartItemSerializer
from cart.models import Cart


User = get_user_model()


class RegisterAPI(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer


class UserListAPI(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]


class LoginAPI(APIView):    
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]
        login(request, user)
        return Response(
            {"detail": "Logged in"}, 
            status=status.HTTP_200_OK
            )


class LogoutAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response(
            {"detail": "logout out successfully"},
            status=status.HTTP_200_OK
            )


class AccountMeAPI(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

    def perform_destroy(self, instance):
        if instance.is_superuser or instance.is_staff:
            raise PermissionDenied("Admin/superuser cannot delete their own account via this endpoint.")
        logout(self.request)
        instance.delete()


class AdminDeleteUserAPI(DestroyAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = "id"
    lookup_url_kwarg = "id"

    def perform_destroy(self, instance):
        if instance.is_superuser:
            raise PermissionDenied("You cannot delete superuser.")
        if instance == self.request.user:
            raise PermissionDenied("You cannot delete yourself.")
        instance.delete()


class PasswordChangeAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(
            data=request.data,
            context={"request": request},
            )
        serializer.is_valid(raise_exception=True)
        user = request.user
        user.set_password(serializer.validated_data["new_password"])
        user.save()

        logout(request)
        return Response({"detail": "Password changed succefully."},
                        status=status.HTTP_200_OK)


class CheckoutAPI(APIView):
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        addresses = Address.objects.filter(user=user)
        cart = Cart.objects.filter(
            user=user,
            status=Cart.Status.DRAFT
        ).select_related('coupon').first()

        if not cart:
            return Response({"message": "سبد خرید خالی است"}, status=400)

        items = cart.items.all()
        final_price = cart.get_final_price()

        return Response({
            'addresses': AddressSerializer(addresses, many=True).data,
            'form': AddressSerializer().data,
            'items': CartItemSerializer(items, many=True).data,
            'final_price': final_price,
        })

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            new_address = serializer.save(user=self.request.user)
            return Response({
                "message": "Address saved successfully",
                "data": serializer.data,
                "new_address_id": new_address.id
            })
        return Response(serializer.errors, status=400)


class ConfirmOrderAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        selected_address_id = request.data.get("selected_address")
        if not selected_address_id:
            return Response(
                {"message": "Address not found"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user = request.user
        address = get_object_or_404(Address, id=selected_address_id, user=user)
        cart = (
            Cart.objects.filter(user=user, status=Cart.Status.DRAFT)
            .select_related('coupon')
            .prefetch_related('items')
            .first()
        )
        if not cart:
            return Response({"message": "The shopping cart is empty."},
                            status=status.HTTP_400_BAD_REQUEST)

        items = cart.items.all()
        final_price = cart.get_final_price()
        shipping_cost = 50000 if address.city == "تهران" else 60000
        total_to_pay = final_price + shipping_cost
        cart.status = Cart.Status.DRAFT
        cart.save()

        return Response(
            {
                "items": CartItemSerializer(items, many=True).data,
                "final_price": final_price,
                "address": AddressSerializer(address).data,
                "shipping_cost": shipping_cost,
                "total_to_pay": total_to_pay,
            },
            status=status.HTTP_201_CREATED,
        )


class ProfileAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response({
            "user": serializer.data,
        })
