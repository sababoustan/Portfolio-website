from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from cart.models import Cart

@shared_task
def clear_old_carts():
    Cart.objects.filter(
        status__in=[Cart.Status.DRAFT, Cart.Status.Rejected],
        created_at__lt=timezone.now() - timedelta(days=30)
    ).delete()