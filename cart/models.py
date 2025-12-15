from django.db import models
import uuid
from django.utils import timezone
from accounts.models import User, Address
from products.models import Product


# Create your models here.
class Coupon(models.Model):
    class Discount_type(models.TextChoices):
        PERCENT = ('p', 'درصدی')
        FIXED = ('fa', 'مبلغ ثابت')
        
    discount_type = models.CharField(default=Discount_type.PERCENT,
                                     max_length=2, 
                                     choices=Discount_type.choices, 
                                     verbose_name='نوع تخفیف')    
    code = models.CharField(max_length=100, verbose_name='کدتخفیف')
    discount_amount = models.DecimalField(default=0, max_digits=10,
                                          decimal_places=0, 
                                          verbose_name='مقدار تخفیف')
    min_order_amount = models.DecimalField(max_digits=10, decimal_places=0, 
                                           verbose_name=
                                           'حداقل مبلغ قابل استفاده')
    valid_from = models.DateTimeField(verbose_name='تاریخ شروع اعتبار', 
                                      blank=True)
    valid_to = models.DateTimeField(verbose_name='تاریخ پایان اعتبار', 
                                    blank=True)
    
    def __str__(self):
        return f"{self.code}"
    
    class Meta:
        verbose_name = 'تخفیف'
        verbose_name_plural = 'تخفیف ها'
        ordering = ['-valid_to']


class Cart(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DF', 'فعال'
        PUBLISHED = 'PB', 'تبدیل شده'
        Rejected = 'RJ', 'حذف شده'
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        User,
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='carts',
        verbose_name='سبدخریدها'
    )
    session_id = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=2, choices=Status.choices, 
                              default=Status.DRAFT, verbose_name='وضعیت')
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, 
                               verbose_name='کد تخفیف', null=True, blank=True, 
                               related_name='used_in_carts')
    total_price = models.DecimalField(max_digits=10, decimal_places=0, 
                                      verbose_name='جمع مبلغ', default=0)
    created_at = models.DateTimeField(default=timezone.now, 
                                      verbose_name='تاریخ ایجاد', blank=True)
    updated_at = models.DateTimeField(auto_now=True, 
                                      verbose_name='زمان اخرین تغییر')
    
    def __str__(self):
        return f"Cart {self.id}"
            
    class Meta:
        verbose_name = 'سبدخرید'
        verbose_name_plural = ' سبدخریدها'
        ordering = ['-created_at']
        
    def update_total_price(self):
        total = self.items.aggregate(total=models.Sum('total_price'))['total'] or 0
        self.total_price = total
        super().save(update_fields=['total_price'])
        
    def get_total_quantity(self):
        return self.items.aggregate(
            total=models.Sum('quantity')
        )['total'] or 0
        
    def get_discount_amount(self):
        if not self.coupon:
            return 0
        
        coupon = self.coupon
        now = timezone.now()
        if not (coupon.valid_from <= now <= coupon.valid_to):
            return 0
        
        if self.total_price < coupon.min_order_amount:
            return 0

        discount_value = float(coupon.discount_amount)
        if coupon.discount_type == Coupon.Discount_type.PERCENT:
            discount = (float(self.total_price) * discount_value)/ 100
            
        else:
            discount = float(coupon.discount_amount)
            
        if discount > float(self.total_price):
            discount = float(self.total_price)
        return int(discount)    
    
    def get_final_price(self):
        return self.total_price - self.get_discount_amount()
    

class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='آیتم ها'
    )
    quantity = models.IntegerField(default=1, verbose_name='تعداد')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, 
                                verbose_name='ایتم های سبدخرید', 
                                related_name='cart_items')
    unit_price = models.DecimalField(max_digits=10, decimal_places=0,
                                     verbose_name='قیمت فعلی', blank=True, 
                                     null=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=0, 
                                      verbose_name='جمع مبلغ', editable=False)
    added_at = models.DateTimeField(default=timezone.now, 
                                    verbose_name='تاریخ اضافه شدن سبد', 
                                    blank=True)
    
    def save(self, *args, **kwargs):
        if not self.unit_price:
            self.unit_price = self.product.price
        self.total_price = self.quantity * self.unit_price
        super().save(*args, **kwargs)
        
        self.cart.update_total_price()
        
    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        self.cart.update_total_price()
    
    class Meta:
        verbose_name = 'آیتم سبدخرید'
        verbose_name_plural = 'آیتم های سبدخرید'
        ordering = ['-added_at']

    def __str__(self):
        return f"{self.product.title} ({self.quantity})"
    
    
class Wishlist(models.Model):
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name='wishlist',
        verbose_name='کاربر')
    product = models.ForeignKey(
        Product, 
        on_delete=models.CASCADE,
        related_name='wishlists',
        verbose_name='محصول')
    added_at = models.DateTimeField(default=timezone.now, 
                                    verbose_name=
                                    'تاریخ اضافه شدن به علاقه مندی ها', 
                                    blank=True)
    
    class Meta:
        verbose_name = 'محصول مورد علاقه'
        verbose_name_plural = 'محصولات موردعلاقه'
        ordering = ['-added_at']
        
    def __str__(self):
        return f"{self.user}-{self.product}"
    
    
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