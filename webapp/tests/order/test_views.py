import pytest
from django.conf import settings
from django.urls import reverse

from orders.models import Order, OrderItem
from shop.factory import ProductFactory


@pytest.fixture
def product():
    return ProductFactory.create()


@pytest.fixture
def client_with_cart(client, product):
    client.post(
        reverse("cart:cart_add", args=[product.id]),
        data={"quantity": 1, "override": False},
    )
    return client


@pytest.mark.django_db
def test_order_create_view(client_with_cart):
    response = client_with_cart.post(
        reverse("orders:order_create"),
        data={
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com",
            "address": "123 Main St",
            "postal_code": "12345",
            "city": "City",
        },
    )

    assert response.status_code == 200
    assert Order.objects.count() == 1
    assert OrderItem.objects.count() == 1
    assert not client_with_cart.session[settings.CART_SESSION_ID]  # 빈 딕셔너리 {}


@pytest.mark.django_db
def test_order_create_view_invalid_form(client, product):
    response = client.post(reverse("orders:order_create"), data={})
    assert response.status_code == 200
    assert Order.objects.count() == 0
    assert OrderItem.objects.count() == 0


@pytest.mark.django_db
def test_order_create_view_empty_cart(client):
    response = client.post(
        reverse("orders:order_create"),
        data={
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com",
            "address": "123 Main St",
            "postal_code": "12345",
            "city": "City",
        },
    )

    assert response.status_code == 200
    assert Order.objects.count() == 0
    assert OrderItem.objects.count() == 0
