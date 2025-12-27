import pytest
from django.contrib.auth import get_user_model
from orders.models import Order
from cart.models import Cart
from accounts.models import Address
from products.models import Product
from orders.models import OrderItem
from products.models import Category

User = get_user_model()


@pytest.fixture
def user(db):
    return User.objects.create_user(
        username="testuser",
        password="123456"
    )


@pytest.fixture
def category(db):
    return Category.objects.create(
        title="Test Category",
        slug="test-category"
    )


@pytest.fixture
def product(db, category):
    return Product.objects.create(
        title="Test Product",
        price=50_000,
        stock=1,
        category=category
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
    

@pytest.fixture
def order_item(db, order, product):
    return OrderItem.objects.create(
        order=order,
        product=product,
        quantity=2,         
        total_price=100_000
    )

