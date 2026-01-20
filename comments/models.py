from django.db import models
from accounts.models import User
from products.models import Product


# Create your models here.
class Comment(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='کاربر'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='محصول'
    )
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='replies',
        verbose_name='پاسخ به'
    )
    body = models.CharField(max_length=250, verbose_name='بدنه کامنت')
    is_active = models.BooleanField(default=True, verbose_name='نمایش در سایت')
    created_at = models.DateTimeField(auto_now_add=True, 
                                      verbose_name='تاریخ انتشار')
    
    def __str__(self):
        return f"{self.user}-{self.body[:30]}"
    
    class Meta:
        verbose_name = 'کامنت'
        verbose_name_plural = 'کامنت ها'
        ordering = ['-created_at']
    