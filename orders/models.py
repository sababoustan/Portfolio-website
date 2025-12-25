from django.db import models
from django.utils import timezone
from accounts.models import User, Address
from cart.models import Cart
from products.models import Product


# Create your models here.
class Order(models.Model):
    class status_order(models.TextChoices):
        Default = ('Created', 'ایجاد شده')
        PendingPayment = ('PendingPayment', ' در انتظار پرداخت')
        Paid = ('Paid', 'پرداخت شده')
        Processing = ('Processing', 'در حال پردازش')
        Shipped = ('Shipped', ' ارسال شده')
        Delivered = ('Delivered', ' تحویل داده شده')
        Canceled = ('Canceled', ' لغو شده')
        Returned = ('Returned', 'مرجوع شده')
        Failed = ('Failed', 'پرداخت ناموفق')
    
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name='order',
        verbose_name='کاربر')
    cart = models.ForeignKey(
            Cart,
            on_delete=models.CASCADE,
            related_name='cart',
            verbose_name='سبدخرید'
        ) 
    address = models.ForeignKey(
            Address,
            on_delete=models.CASCADE,
            related_name='address',
            verbose_name='آدرس'
        )
    status = models.CharField(max_length=50, choices=status_order.choices, 
                               default=status_order.Default, verbose_name=
                               'وضعیت پرداخت')
    created_at = models.DateTimeField(default=timezone.now,
                                      verbose_name='تاریخ ثبت سفارش')
    payment_tracking_code = models.CharField(max_length=100, null=True,
                                             blank=True)
    authority = models.CharField(max_length=100, null=True, blank=True)
    total_price = models.PositiveIntegerField()
    order_note = models.TextField(null=True, blank=True, 
                                  verbose_name="توضیحات سفارش")

    def get_total_price(self):
        return self.cart.get_final_price()   
    
    def save(self, *args, **kwargs):
        self.total_price = self.get_total_price()
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = 'وضعیت سفارش'
        verbose_name_plural = 'وضعیت سفارش ها'
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.user}-{self.authority}"


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='سفارش'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='order_item',
        verbose_name='محصول'
    )
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.PositiveIntegerField()
    
    class Meta:
        verbose_name = 'ایتم سفارش'
        verbose_name_plural = 'ایتم های سفارش'
        
    def __str__(self):
        return f"{self.product.title} - {self.quantity} عدد"