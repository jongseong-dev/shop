import pytest
import redis

from shop.factory import ProductFactory
from shop.recommender import Recommender


@pytest.fixture
def products():
    return ProductFactory.create_batch(size=10)


@pytest.fixture
def redis_client(request) -> redis.Redis:
    import fakeredis

    return fakeredis.FakeRedis()


@pytest.fixture
def recommender(redis_client):
    return Recommender(redis_client)


@pytest.mark.django_db
def test_products_bought(redis_client, recommender, products):
    recommender.products_bought(products)
    for product in products:
        for other in products:
            if product != other:
                assert (
                    int(
                        redis_client.zscore(
                            recommender.get_product_key(product.id), other.id
                        )
                    )
                    == 1
                )


@pytest.mark.django_db
def test_suggest_products_for(redis_client, recommender, products):
    recommender.products_bought(products)
    suggestions = recommender.suggest_products_for(products[:1], max_results=2)
    expected_results = redis_client.zrange(
        recommender.get_product_key(products[0].id), 0, -1, desc=True
    )
    assert len(suggestions) == 2
    assert suggestions[0].id == int(expected_results[0])
    assert suggestions[1].id == int(expected_results[1])


@pytest.mark.django_db
def test_clear_purchases(redis_client, recommender, products):
    recommender.products_bought(products)
    recommender.clear_purchases()
    for product in products:
        assert (
            redis_client.zscore(
                recommender.get_product_key(product.id), products[0].id
            )
            is None
        )
