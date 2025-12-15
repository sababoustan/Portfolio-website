from django import forms
from .models import User, Address


class LoginForm(forms.Form):
    username_or_email = forms.CharField(label="نام کاربری یا آدرس ایمیل", 
                                         max_length=250, 
                                         required=True, 
                                         widget=forms.TextInput(attrs={
                                        'class': 'form-control',
                                        'placeholder': 
                                        'نام کاربری یا آدرس ایمیل'
        }))
    password = forms.CharField(label="کلمه عبور", max_length=250, 
                               required=True, widget=forms.PasswordInput(attrs={
                                'class': 'form-control',
                                'placeholder': 'کلمه عبور'
        }))

  
class RegisterForm(forms.ModelForm):
    password = forms.CharField(label='پسورد', max_length=250, required=True, 
                               widget=forms.PasswordInput(attrs={
                                'class': 'form-control',
                                'placeholder': 'پسورد'
    }))
    
    class Meta:
        model = User
        fields = ['username','email']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'نام کاربری'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'ایمیل'
            }),
        }
        
        
class AddressForm(forms.ModelForm):
    
    class Meta:
        model = Address
        fields = ['full_name', 'city', 'street_address', 'postal_code', 
                'phone_number']
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'نام گیرنده'
            }),
            'city': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'شهر'
            }),
            'street_address': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'آدرس'
            }),
            'postal_code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'کدپستی'
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'شماره تماس'
            }),
        }
        
