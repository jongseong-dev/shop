import pytest
import stripe
from django.test import RequestFactory
from unittest.mock import patch
from orders.models import Order
from payment.webhooks import stripe_webhook


@pytest.fixture
def factory():
    return RequestFactory()


@pytest.fixture
def order():
    return Order.objects.create(id=1, paid=False)


@patch("stripe.Webhook.construct_event")
@pytest.mark.django_db
def test_stripe_webhook_valid_payload(mock_construct_event, factory, order):
    mock_construct_event.return_value = type(
        "Mock",
        (),
        {
            "type": "checkout.session.completed",
            "data": type(
                "Mock",
                (),
                {
                    "object": type(
                        "Mock",
                        (),
                        {
                            "mode": "payment",
                            "payment_status": "paid",
                            "client_reference_id": order.id,
                            "payment_intent": "pi_123",
                        },
                    )
                },
            ),
        },
    )
    request = factory.post("/webhook/", HTTP_STRIPE_SIGNATURE="t=123")
    response = stripe_webhook(request)
    order.refresh_from_db()
    assert response.status_code == 200
    assert order.paid
    assert order.stripe_id == "pi_123"


@patch("stripe.Webhook.construct_event")
@pytest.mark.django_db
def test_stripe_webhook_invalid_payload(mock_construct_event, factory):
    mock_construct_event.side_effect = ValueError
    request = factory.post("/webhook/", HTTP_STRIPE_SIGNATURE="t=123")
    response = stripe_webhook(request)
    assert response.status_code == 400


@patch("stripe.Webhook.construct_event")
@pytest.mark.django_db
def test_stripe_webhook_invalid_signature(mock_construct_event, factory):
    mock_construct_event.side_effect = stripe.error.SignatureVerificationError(
        "message", "sig_header"
    )
    request = factory.post("/webhook/", HTTP_STRIPE_SIGNATURE="t=123")
    response = stripe_webhook(request)
    assert response.status_code == 400


@patch("stripe.Webhook.construct_event")
@pytest.mark.django_db
def test_stripe_webhook_order_does_not_exist(mock_construct_event, factory):
    mock_construct_event.return_value = type(
        "Mock",
        (),
        {
            "type": "checkout.session.completed",
            "data": type(
                "Mock",
                (),
                {
                    "object": type(
                        "Mock",
                        (),
                        {
                            "mode": "payment",
                            "payment_status": "paid",
                            "client_reference_id": 999,
                            "payment_intent": "pi_123",
                        },
                    )
                },
            ),
        },
    )
    request = factory.post("/webhook/", HTTP_STRIPE_SIGNATURE="t=123")
    response = stripe_webhook(request)
    assert response.status_code == 404
