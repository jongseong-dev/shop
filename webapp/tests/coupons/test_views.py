import pytest
from django.urls import reverse

from coupons.factory import CouponFactory


@pytest.fixture
def coupon():
    return CouponFactory.create()


@pytest.fixture
def coupon_apply_url():
    return reverse("coupons:apply")


@pytest.fixture
def cart_url():
    return reverse("cart:cart_detail")


@pytest.mark.django_db
def test_coupon_apply_valid_coupon(client, coupon_apply_url, cart_url, coupon):
    response = client.post(coupon_apply_url, {"code": coupon.code})
    assert response.status_code == 302
    assert response.url == cart_url
    assert client.session["coupon_id"] == coupon.id


@pytest.mark.django_db
def test_coupon_apply_invalid_coupon(client, cart_url, coupon_apply_url):
    response = client.post(coupon_apply_url, {"code": "invalid"})
    assert response.status_code == 302
    assert response.url == cart_url
    assert client.session["coupon_id"] is None
