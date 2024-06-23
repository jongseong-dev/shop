import pytest
from django.urls import reverse
from orders.factory import OrderFactory
from unittest.mock import patch


@pytest.fixture
def order():
    return OrderFactory.create()


@patch("stripe.checkout.Session.create")
@pytest.mark.django_db
def test_payment_process_post(mock_stripe_create, client, order):
    mock_stripe_create.return_value = type(
        "Mock", (), {"url": "http://test.url"}
    )
    session = client.session
    session["order_id"] = order.id
    session.save()
    response = client.post(reverse("payment:process"))
    assert response.status_code == 302
    assert response.url == "http://test.url"


@pytest.mark.django_db
def test_payment_process_get(client, order):
    session = client.session
    session["order_id"] = order.id
    session.save()
    response = client.get(reverse("payment:process"))
    assert response.status_code == 200


@pytest.mark.django_db
def test_payment_completed(client):
    response = client.get(reverse("payment:completed"))
    assert response.status_code == 200


@pytest.mark.django_db
def test_payment_canceled(client):
    response = client.get(reverse("payment:canceled"))
    assert response.status_code == 200
