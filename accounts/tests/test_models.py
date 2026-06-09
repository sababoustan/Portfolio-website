import pytest
from accounts.models import User


@pytest.mark.django_db
def test_create_user(user):
    assert user.username == "testuser"


@pytest.mark.django_db
def test_create_address(address):
    assert address.pk is not None