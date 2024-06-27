import factory
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyInteger
from coupons.models import Coupon


class CouponFactory(DjangoModelFactory):
    class Meta:
        model = Coupon

    code = factory.Faker("pystr", max_chars=50)
    valid_from = factory.Faker("past_datetime")
    valid_to = factory.Faker("future_datetime")
    discount = FuzzyInteger(0, 100)
    active = factory.Faker("boolean")
