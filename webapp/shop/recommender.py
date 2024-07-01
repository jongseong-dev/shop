import redis
from django.conf import settings

from shop.models import Product


# Reids 연결
class RedisSingleton:
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = redis.Redis(
                host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                db=settings.REDIS_DB,
            )
        return cls._instance


cache_instance = RedisSingleton.get_instance()


class Recommender:
    """
    제품 구매 내역을 저장하고 특정 제품에 맞는 추천 제품을 조회할 수 있는 클래스
    """

    def __init__(self, cache_storage=None):
        if cache_storage is not None:
            self._cache_storage = cache_storage
        else:
            self._cache_storage = cache_instance

    def get_product_key(self, id):
        return f"product:{id}:purchased_with"

    def products_bought(self, products):
        """
        함꼐 구매한 제품을 저장하고 점수를 매기는 method
        :param products:
        :return:
        """
        product_ids = [p.id for p in products]
        for product_id in product_ids:
            for with_id in product_ids:
                # 각 제품과 함께 구매한 다른 제품 획득
                if product_id != with_id:
                    # 함께 구매한 제품의 점수 증가
                    self._cache_storage.zincrby(
                        self.get_product_key(product_id), 1, with_id
                    )

    def suggest_products_for(self, products, max_results=6):
        products_ids = [p.id for p in products]
        if len(products) == 1:
            # 단 1개의 제품
            suggestions = self._cache_storage.zrange(
                self.get_product_key(products_ids[0]), 0, -1, desc=True
            )[:max_results]
        else:
            # 임시 키 생성
            flat_ids = "".join([str(id) for id in products_ids])
            tmp_key = f"tmp_{flat_ids}"
            # 주어진 각 제품들에 함께 구매한 제품들의 점수 합산
            # 결과가 정렬된 세트를 임시 키에 저장
            keys = [self.get_product_key(id) for id in products_ids]
            self._cache_storage.zunionstore(
                tmp_key, keys
            )  # zuninstaore: 주어진 키들에 해당하는 정렬된 집합들에 대해
            # 유니온을 수행하면서 동일한 요소들의 점수를 집계한다.

            # 처음에 주어진 제품들의 ID를 추천 목록에서 제거, 동일한 제품이 추천목록에 뜨는 것을 방지
            self._cache_storage.zrem(tmp_key, *products_ids)
            # 점수를 기준으로 역정렬해서 제품 id 목록을 가져옴
            suggestions = self._cache_storage.zrange(
                tmp_key, 0, -1, desc=True
            )[:max_results]
            # 임시 키 제거
            self._cache_storage.delete(tmp_key)

        suggested_products_ids = [int(id) for id in suggestions]
        # 추천 제품 정보 조회 및 순서대로 정렬해 표시
        suggested_products = list(
            Product.objects.filter(id__in=suggested_products_ids)
        )
        suggested_products.sort(
            key=lambda x: suggested_products_ids.index(x.id)
        )
        return suggested_products

    def clear_purchases(self):
        for id in Product.objects.values_list("id", flat=True):
            self._cache_storage.delete(self.get_product_key(id))
