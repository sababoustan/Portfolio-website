from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError
from cart.api.serializers import (
    CartSerializer,
    AddToCartInputSerializer,
    CartActionSerializer,
    CouponSerializer,
    WishListSerializer
)
from rest_framework.authentication import TokenAuthentication
from cart.models import Cart, CartItem, Coupon, Wishlist
from products.models import Product
from rest_framework import status
from rest_framework.response import Response


class CartAPI(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        cart = get_object_or_404(Cart, user=request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data)
    
    
class CartItemAPI(APIView):
    permission_classes = [IsAuthenticated]
    
    def delete(self, request, item_id):
        
        item = get_object_or_404(
            CartItem,
            id=item_id,
            cart__user=request.user,
        )
        cart = item.cart
        item.delete()
        cart.refresh_from_db()
        return Response(CartSerializer(cart).data, status=status.HTTP_200_OK)
    
    
class AddToCartAPI(GenericAPIView):
    serializer_class = AddToCartInputSerializer
    permission_classes = [IsAuthenticated]
    
    def get_cart(self, request):
        if request.user.is_authenticated:
            cart, _ = Cart.objects.get_or_create(
                user=request.user,
                status=Cart.Status.DRAFT
            )
            return cart
        
        if not request.session.session_key:
            request.session.create()
            
        cart, _ = Cart.objects.get_or_create(
            user=request.user,
            status=Cart.Status.DRAFT
            )
        return cart

    def post(self, request):
        inp = self.get_serializer(data=request.data)
        inp.is_valid(raise_exception=True)
        product_id = inp.validated_data["product_id"]
        qty = inp.validated_data["qty"]
        cart = self.get_cart(request)
        product = get_object_or_404(Product, id=product_id)
        item = cart.items.filter(product_id=product.id).first()
        if item:
            new_qty = item.quantity + qty
            if new_qty > product.stock:
                raise ValidationError({"qty":"این تعداد بیشتر از موجودی محصول است"})
            item.quantity = new_qty
            item.save()
        else:
            if qty > product.stock:
                raise ValidationError({"qty":"این تعداد موجود نیست"})
            CartItem.objects.create(
                cart=cart,
                product=product,
                unit_price=product.price,
                quantity=qty
            )
            cart.refresh_from_db()
        return Response(CartSerializer(cart).data, status=status.HTTP_200_OK)
    
    
class UpdateCartAPI(APIView):
    serializer_class = CartActionSerializer
    permission_classes = [IsAuthenticated]
    
    def get_cart(self, request):
        cart, _ = Cart.objects.get_or_create(
                user=request.user,
                status=Cart.Status.DRAFT
            )
        return cart
    
    def update_item(self, action, cart, product_id):
        product = get_object_or_404(Product, id=product_id)
        item = cart.items.filter(product_id=product.id).first()
        if not item:
            raise ValidationError({"detail": "Item not found"})
        removed = False 
        
        if action == "increase":
            if item.quantity >= item.product.stock:
                raise ValidationError({
                    "detail": "حداکثر موجودی محصول همین تعداد است",
                    "error": "max_stock"
                })
            item.quantity += 1
            item.save()
            
        elif action == "decrease":
            if item.quantity > 1:
                item.quantity -= 1
                item.save()
            else:
                item.delete()
                removed = True
        cart.refresh_from_db()
        return {
            "removed": removed,
            "quantity": item.quantity if not removed else 0,
            "item_total": item.total_price if not removed else 0,
            "cart_total": cart.total_price,
            "discount": cart.get_discount_amount(),
            "final_total": cart.get_final_price(),
            "cart_count": cart.get_total_quantity(),
        }
        
    def post(self, request):
        inp = self.serializer_class(data=request.data)
        inp.is_valid(raise_exception=True)
        product_id = inp.validated_data["product_id"]
        action = inp.validated_data["action"]
        cart = self.get_cart(request=request)
        data = self.update_item(
            cart=cart,
            product_id=product_id,
            action=action
        )
        return Response(data, status=status.HTTP_200_OK)
            
    
class CouponAPI(APIView):
    serializer_class = CouponSerializer
    permission_classes = [IsAuthenticated]
    
    def get_cart(self, request):
        cart, _ = Cart.objects.get_or_create(
                user=request.user,
                status=Cart.Status.DRAFT
            )
        return cart
    
    def apply(self, cart, code):
        if not code:
            raise ValueError("EMPTY CODE")
        coupon = Coupon.objects.filter(code=code).first()
        if not coupon:
            raise ValueError("INVALID_CODE")
        cart.coupon = coupon
        cart.save()
        discount = cart.get_discount_amount()
        if discount == 0:
            raise ValueError("CONDITION_NOT_MET")
        return discount
        
    def post(self, request):
        cart = self.get_cart(request=request)
        inp = self.serializer_class(data=request.data)
        inp.is_valid(raise_exception=True)
        code = inp.validated_data["code"]
        try:
            discount = self.apply(cart, code)
        except ValueError as e:
            if str(e) == "EMPTY_CODE":
                return Response(
                    {
                        "error": "EMPTY_CODE",
                        "message": "کد تخفیف وارد نشده است"
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
            elif str(e) == "INVALID_CODE":
                return Response(
                    {
                        "error": "INVALID_CODE",
                        "message": "کد تخفیف اشتباه است"
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
            elif str(e) == "CONDITION_NOT_MET":
                return Response(
                    {
                        "error": "CONDITION_NOT_MET",
                        "message": "شرایط اعمال کد تخفیف رعایت نشده است"
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
        return Response(
            {
                "discount": discount,
                "final_price": cart.get_final_price,
                "message": "کد تخفیف با موفقیت اعمال شد"
            },
            status=status.HTTP_200_OK
        )

        
class WishlistAPI(APIView):
    permission_classes = [IsAuthenticated]
        
    def get(self, request):
        wishlists = Wishlist.objects.filter(user=request.user)
        serializer = WishListSerializer(wishlists, many=True)
        return Response(serializer.data)


class WishlistToggleAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        wishlist_item = Wishlist.objects.filter(
            user=request.user,
            product=product
        ).first()
        if wishlist_item:
            wishlist_item.delete()
            status = "removed"
        else:
            Wishlist.objects.create(
                user=request.user,
            product=product
            )
            status="added"
        wishlist_count = Wishlist.objects.filter(user=request.user,).count()
        return Response({
            "status": status,
            "wishlist_count": wishlist_count
        })