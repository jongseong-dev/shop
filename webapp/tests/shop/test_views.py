import pytest
from django.test import RequestFactory
from django.urls import reverse

from shop.factory import ProductFactory, CategoryFactory


@pytest.fixture
def url_product_list():
    return reverse("shop:product_list")


@pytest.fixture
def factory():
    return RequestFactory()


@pytest.fixture
def category():
    return CategoryFactory.create()


@pytest.fixture
def product_available(category):
    return ProductFactory.create(available=True, category=category)


@pytest.fixture
def product_unavailable(category):
    return ProductFactory.create(available=False, category=category)


@pytest.mark.django_db
def test_product_list_with_category(
    client, url_product_list, category, product_available, product_unavailable
):
    response = client.get(f"{url_product_list}{category.slug}/")
    assert response.status_code == 200
    assert product_available in response.context["products"]
    assert product_unavailable not in response.context["products"]


@pytest.mark.django_db
def test_product_list_without_category(
    client, url_product_list, product_available
):
    response = client.get(url_product_list)
    assert response.status_code == 200
    assert product_available in response.context["products"]


@pytest.mark.django_db
def test_product_detail(client, url_product_list, product_available):
    response = client.get(
        f"{url_product_list}{product_available.id}/{product_available.slug}/"
    )
    assert response.status_code == 200
    assert response.context["product"] == product_available


@pytest.mark.django_db
def test_product_detail_with_unavailable_product(
    client, url_product_list, product_unavailable
):
    path = f"{product_unavailable.id}/{product_unavailable.slug}/"
    response = client.get(f"{url_product_list}{path}")
    assert response.status_code == 404
