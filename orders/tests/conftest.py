import pytest
from django.contrib.auth import get_user_model
from orders.models import Order
from cart.models import Cart
from accounts.models import Address

User = get_user_model()


@pytest.fixture
def user(db):
    return User.objects.create_user(
        username="testuser",
        password="123456"
    )


@pytest.fixture
def cart(db, user):
    return Cart.objects.create(user=user)


@pytest.fixture
def address(db, user):
    return Address.objects.create(
        user=user,
        full_name="Test User",
        city="Tehran",
        street_address="Test street",
        postal_code="1234567890",
        phone_number="09123456789"
    )


@pytest.fixture
def order(db, user, cart, address):
    return Order.objects.create(
        user=user,
        cart=cart,
        address=address,
        status=Order.status_order.Default,
        total_price=100_000
    )
