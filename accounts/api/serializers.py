from rest_framework import serializers
from accounts.models import Address
from django.contrib.auth import authenticate, get_user_model


User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        label="پسورد",
        write_only=True,
        min_length=8,
    )
    
    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password"
        ]
    
    def create(self, validated_data):
        user = User(
            username=validated_data["username"],
            email=validated_data["email"],   
        )
        user.set_password(validated_data["password"])
        user.save()
        return user
  
  
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
        ]
       
        
        
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True, 
                                         trim_whitespace=False)
    new_password = serializers.CharField(write_only=True, min_length=8, 
                                         trim_whitespace=False)
    new_password2 = serializers.CharField(write_only=True, min_length=8, 
                                          trim_whitespace=False)
    
    def validate_old_password(self, value):
        user = self.context["request"].user
        if not user.check_password(value):
            raise serializers.ValidationError("رمز فعلی اشتباه است.")
        return value
    
    def validate(self, attrs):
        new_passwrod = attrs.get("new_password")
        new_passwrod2 = attrs.get("new_password2")
        
        if new_passwrod != new_passwrod2:
            raise serializers.ValidationError({"new_password2": "تکرار رمز با رمز یکسان نیست."})
        
        if attrs.get("old_password") == new_passwrod:
            raise serializers.ValidationError({"new_password": "رمز جدید نباید با رمز قدیمی یکسان باشد"})
        
        return attrs
          
class LoginSerializer(serializers.Serializer):
    username_or_email = serializers.CharField()
    password = serializers.CharField(write_only=True, trim_whitespace=False)
    
    def validate(self, attrs):
        identifier = attrs.get("username_or_email")
        password = attrs.get("password")
        
        if not identifier or not password:
            raise serializers.ValidationError("نام کاربری/ایمیل و رمز عبور الزامی است.")
        
        if "@" in identifier:
            try:
                user_obj = User.objects.get(email__iexact=identifier)
                username = user_obj.get_username()
            except User.DoesNotExist:
                raise serializers.ValidationError("ایمیل یا رمز عبور اشتباه است.")
        else:
            username = identifier
        user = authenticate(username=username, password=password)

        if not user:
            raise serializers.ValidationError("نام کاربری/ایمیل یا رمز عبور اشتباه است.")
        
        if not user.is_active:
            raise serializers.ValidationError("حساب کاربری غیرفعال است.")
        
        attrs["user"] = user
        return attrs
        

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = [
            "username",
            "city",
            "street_address",
            "postal_code",
            "phone_number"
        ]