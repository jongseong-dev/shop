from decimal import Decimal

import pytest
from django.urls import reverse

from cart.cart import Cart
from coupons.factory import CouponFactory
from shop.factory import ProductFactory


@pytest.fixture
def product():
    return ProductFactory.create()


@pytest.fixture
def coupon():
    return CouponFactory.create()


@pytest.fixture
def client_with_cart_and_coupon(client, product, coupon):
    client.post(reverse("coupons:apply"), data={"code": coupon.code})
    client.post(
        reverse("cart:cart_add", args=[product.id]),
        data={"quantity": 1, "override": False},
    )
    return client


@pytest.mark.django_db
def test_cart_initialization(client):
    cart = Cart(client)
    assert len(cart) == 0


@pytest.mark.django_db
def test_cart_add_product_no_coupon(client, product):
    cart = Cart(client)
    cart.add(product=product, quantity=2)
    assert len(cart) == 2
    assert cart.get_discount() == 0


@pytest.mark.django_db
def test_cart_remove_product(client, product):
    cart = Cart(client)
    cart.add(product=product, quantity=2)
    cart.remove(product=product)
    assert len(cart) == 0


@pytest.mark.django_db
def test_cart_apply_coupon(client, product, coupon):
    cart = Cart(client)
    cart.add(product=product, quantity=2)
    cart.coupon_id = coupon.id
    assert (
        cart.get_discount()
        == coupon.discount / Decimal(100) * cart.get_total_price()
    )
    assert (
        cart.get_total_price_after_discount()
        == cart.get_total_price() - cart.get_discount()
    )
