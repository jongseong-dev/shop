from decimal import Decimal

from django.conf import settings

from shop.models import Product


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID, {})
        if not cart:
            # 세션에 카트가 없으면 빈 딕셔너리를 저장
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(
        self,
        product: Product,
        quantity: int = 1,
        override_quantity: bool = False,
    ):
        """
        Add a product to the cart ro update its quantity.
        :param product: 카트에 추가허거나 업데이트할 제품의 인스턴스
        :param quantity: 제품의 수량
        :param override_quantity: 지정된 수량으로 수량을 재정의해야 하는지(True)
        또는 기존 수량에 새로운 수량을 추가해야하는지(False)를 나태내는 플래그
        :return:
        """
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {
                "quantity": 0,
                "price": str(product.price),
            }
        if override_quantity:
            self.cart[product_id]["quantity"] = quantity
        else:
            self.cart[product_id]["quantity"] += quantity
        self.save()

    def save(self):
        # 세션을 "modified"으로 표시하여 저장하도록 함
        # 이렇게 세션이 변경되었으므르 저장해야 한다고 장고에게 알리는 역할
        self.session.modified = True

    def remove(self, product: Product):
        """
        Remove a product from the cart.
        :param product: 카트에서 제거할 제품의 인스턴스
        :return:
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        """
        Iterate over the items in the cart
        and get the products from the database.
        :return:
        """
        product_ids = self.cart.keys()
        # Product 객체를 가져와 카트에 추가
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]["product"] = product

        for item in cart.values():
            item["price"] = Decimal(item["price"])
            item["total_price"] = item["price"] * item["quantity"]
            yield item

    def __len__(self):
        """
        Count all items in the cart.
        :return:
        """
        return sum(item["quantity"] for item in self.cart.values())

    def get_total_price(self):
        return sum(
            Decimal(item["price"]) * item["quantity"]
            for item in self.cart.values()
        )

    def clear(self):
        # 카트 비우기
        del self.session[settings.CART_SESSION_ID]
        self.save()
