from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from accounts.models import User
from .models import Cart


@receiver(user_logged_in, sender=User)
def user_login(sender, user, request, **kwargs):
    session_id = request.session.session_key
    cart = Cart.objects.filter(session_id=session_id, user__isnull=True,
                               status='DF').first()
    if cart:
        cart.user = user
        cart.save()

        