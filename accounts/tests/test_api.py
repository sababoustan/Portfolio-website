import pytest
from django.urls import reverse
from django.test import Client


@pytest.mark.django_db
def test_token_api(tokens):
    assert "access" in tokens
    assert "refresh" in tokens

@pytest.mark.django_db
def test_refresh_token_api(tokens):
    client = Client()
    response = client.post(
        "/api/accounts/token/refresh/",
        {
            "refresh": tokens["refresh"],
        }
    )

    assert response.status_code == 200
    assert "access" in response.json()

@pytest.mark.django_db
def test_register(register):
    print(register.json())
    assert register.status_code == 201