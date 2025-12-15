from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    username = models.CharField(max_length=11, unique=True, 
                                verbose_name='نام کاربری', 
                                help_text='فقط حروف، اعداد و @/./+/-/_.')
    email = models.EmailField(unique=True, verbose_name='ایمیل', 
                              help_text='ایمیل کاربر(برای ورود یا بازیابی رمز عبور)')
    date_joined = models.DateTimeField(auto_now_add=True, 
                                       verbose_name='تاریخ عضویت')

    def __str__(self):
        return f"{self.username or self.email}"
    
    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'
        ordering = ['-date_joined']    
     
        
class Address(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='addresses',
        verbose_name='ادرس'
    )
    full_name = models.CharField(max_length=100, blank=False, verbose_name='نام و نام خانوادگی')
    city = models.CharField(max_length=100, blank=False, verbose_name='شهر')
    street_address = models.CharField(max_length=300, blank=False, 
                                      verbose_name='ادرس')
    postal_code = models.CharField(max_length=12, blank=False,
                                   verbose_name='کدپستی')
    phone_number = models.CharField(max_length=11, blank=False,
                                  verbose_name='شماره تماس')
    
    def __str__(self):
        return f"{self.city}-{self.street_address}"
    
    class Meta:
        verbose_name = 'آدرس'
        verbose_name_plural = 'آدرس‌ها'
        ordering = ['-id']
