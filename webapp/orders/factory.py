import factory
from factory.django import DjangoModelFactory

from orders.models import Order, OrderItem
from shop.factory import ProductFactory


class OrderFactory(DjangoModelFactory):
    class Meta:
        model = Order

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    email = factory.Faker("email")
    address = factory.Faker("address")
    postal_code = factory.Faker("zipcode")
    city = factory.Faker("city")
    paid = factory.Faker("boolean")


class OrderItemFactory(DjangoModelFactory):
    class Meta:
        model = OrderItem

    order = factory.SubFactory(OrderFactory)
    product = factory.SubFactory(ProductFactory)
    price = factory.Faker(
        "pydecimal", left_digits=3, right_digits=2, positive=True
    )
    quantity = factory.Faker("random_int", min=1, max=5)
