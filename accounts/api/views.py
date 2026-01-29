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
from rest_framework import status
from accounts.api.serializers import (
    UserSerializer, LoginSerializer, RegisterSerializer, 
    ChangePasswordSerializer)
from accounts.models import Address


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