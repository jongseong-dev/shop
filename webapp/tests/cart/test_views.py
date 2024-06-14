import pytest
from django.urls import reverse

from cart.cart import Cart
from shop.factory import ProductFactory


@pytest.fixture
def product():
    return ProductFactory.create()


@pytest.mark.django_db
def test_cart_add_valid_form(client, product):
    response = client.post(
        reverse("cart:cart_add", args=[product.id]),
        data={"quantity": 1, "override": False},
    )
    assert response.status_code == 302
    cart = Cart(client)
    assert cart.__len__() == 1


@pytest.mark.django_db
def test_cart_add_invalid_form(client, product):
    response = client.post(
        reverse("cart:cart_add", args=[product.id]),
        data={"quantity": 0, "override": False},
    )
    assert response.status_code == 302
    cart = Cart(client)
    assert cart.__len__() == 0


@pytest.mark.django_db
def test_cart_remove_product(client, product):
    client.post(
        reverse("cart:cart_add", args=[product.id]),
        data={"quantity": 1, "override": False},
    )
    response = client.post(reverse("cart:cart_remove", args=[product.id]))
    assert response.status_code == 302
    cart = Cart(client)
    assert cart.__len__() == 0


@pytest.mark.django_db
def test_cart_detail_view(client, product):
    client.post(
        reverse("cart:cart_add", args=[product.id]),
        data={"quantity": 1, "override": False},
    )
    response = client.get(reverse("cart:cart_detail"))
    assert response.status_code == 200
    assert "cart" in response.context
    assert response.context["cart"].__len__() == 1
