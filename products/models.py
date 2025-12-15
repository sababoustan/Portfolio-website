from django.db import models
from django.utils.text import slugify
from django.utils import timezone


# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:  
            self.slug = slugify(self.title, allow_unicode=True)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'
     
        
class Product(models.Model):
    title = models.CharField(max_length=200, verbose_name='عنوان')
    description = models.TextField(max_length=200, 
                                   blank=True, verbose_name='ـوضیحات')
    price = models.DecimalField(max_digits=10, verbose_name=' قیمت پایه', 
                                decimal_places=0)
    discount_price = models.DecimalField(max_digits=10, decimal_places=0, 
                                         null=True, 
                                         verbose_name='قیمت با تخفیف')
    stock = models.IntegerField(verbose_name='موجودی انبار')
    sku = models.CharField(max_length=100, unique=True, verbose_name='کد محصول')
    is_active = models.BooleanField(default=True, verbose_name='نمایش در سایت')
    created_at = models.DateTimeField(default=timezone.now, 
                                      verbose_name='تاریخ ثبت')
    image = models.ImageField(upload_to="product_images/%Y/%m/%d", blank=True, 
                              null=True, verbose_name='عکس محصول')
    slug = models.SlugField(unique=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)  
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            num = 1
            while Product.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{num}"
                num += 1
            self.slug = slug
        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'محصول'
        verbose_name_plural = 'محصولات'
        ordering = ['-created_at'] 


    