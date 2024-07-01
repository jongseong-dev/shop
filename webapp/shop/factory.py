import factory
from django.utils.text import slugify
from factory.django import DjangoModelFactory

from shop.models import Category, Product


class CategoryFactory(DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.Sequence(lambda n: f"Category {n}")
    slug = factory.LazyAttribute(lambda obj: slugify(obj.name))


class ProductFactory(DjangoModelFactory):
    class Meta:
        model = Product

    category = factory.SubFactory(CategoryFactory)
    name = factory.Sequence(lambda n: f"Product {n}")
    slug = factory.LazyAttribute(lambda obj: slugify(obj.name))
    image = factory.django.ImageField(color="blue")
    description = factory.Faker("paragraph")
    price = factory.Faker(
        "pydecimal", left_digits=3, right_digits=2, positive=True
    )
    available = factory.Faker("boolean")
