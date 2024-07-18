import factory
import factory.fuzzy
from django.core.files import File

from ...models import Author, Product, ProductCategory, Publisher


class ProductCategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductCategory

    name = factory.fuzzy.FuzzyText()


class PublisherFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Publisher

    name = factory.Faker("name")


class AuthorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Author

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    name = factory.fuzzy.FuzzyText()
    description = factory.fuzzy.FuzzyText()
    price = factory.fuzzy.FuzzyDecimal(low=0.00)
    quantity = factory.fuzzy.FuzzyInteger(0, 5)
    image = None

    category = factory.SubFactory(ProductCategoryFactory)
    publisher = factory.SubFactory(PublisherFactory)

    isbn = factory.Faker("isbn13")
    page_count = factory.fuzzy.FuzzyInteger(10, 100)
    publication_year = factory.Faker("year")

    class Params:
        with_image = factory.Trait(
            image=factory.django.ImageField(
                from_path="products/tests/test_data/test_img.jpeg"
            )
        )

    @factory.post_generation
    def author(self, create, extracted, **kwargs):
        if not create or not extracted:
            return

        self.author.add(*extracted)
