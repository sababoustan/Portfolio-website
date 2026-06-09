import pytest
from accounts.models import User, Address
from django.test import Client


@pytest.fixture
def user(db):
    return User.objects.create_user(
        username="testuser",
        password="123456"
    )
    
@pytest.fixture
def address(db, user):
    return Address.objects.create(
        user=user,
        full_name="saba",
        city="tehran",
        street_address="ahang highway",
        postal_code="987654323",
        phone_number="09307190078"
    )
    

@pytest.fixture
def tokens(user):
    client = Client()

    response = client.post(
        "/api/accounts/token/",
        {
            "username": "testuser",
            "password": "123456"
        }
    )

    return response.json()

@pytest.fixture
def register():
    client = Client()

    response = client.post(
        "/api/accounts/register/",
        {
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "12345667"
        }
    )
    return response