import pytest
from django.core.exceptions import ValidationError
from orders.models import Order
from orders.services import verify_and_pay_order


@pytest.mark.django_db
def test_verify_paid_order_success(mocker, order):
    mocker.patch(
        "orders.services.requests.post",
        return_value=mocker.Mock(
            json=lambda: {
                "result": 100,
                "refNumber": "TEST-123"
            }
        )
    )
    verify_and_pay_order(order, "123")
    order.refresh_from_db()
    assert order.status == Order.status_order.Paid
    assert order.ref_id == "TEST-123"
    
    
@pytest.mark.django_db
def test_verify_already_paid_order(order):
    order.status = Order.status_order.Paid
    order.save()
    result = verify_and_pay_order(order, "123")
    assert result.status == Order.status_order.Paid
    
@pytest.mark.django_db
def test_payment_getway_failure(mocker, order):
    mocker.patch(
        "orders.services.requests.post",
        return_value=mocker.Mock(
            json=lambda: {"result": -1}
        )
    )
    with pytest.raises(ValidationError):
        verify_and_pay_order(order, "123")
    
