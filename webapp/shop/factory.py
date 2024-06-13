import factory
from factory.django import DjangoModelFactory
from shop.models import Category, Product


class CategoryFactory(DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.Faker("word")
    slug = factory.LazyAttribute(lambda obj: obj.name.lower())


class ProductFactory(DjangoModelFactory):
    class Meta:
        model = Product

    category = factory.SubFactory(CategoryFactory)
    name = factory.Faker("word")
    slug = factory.LazyAttribute(lambda obj: obj.name.lower())
    image = factory.django.ImageField(color="blue")
    description = factory.Faker("paragraph")
    price = factory.Faker(
        "pydecimal", left_digits=3, right_digits=2, positive=True
    )
    available = factory.Faker("boolean")
