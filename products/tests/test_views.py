from django.conf import settings
from django.test import TestCase, override_settings
from django.urls import reverse

from .tests_helpers.factories import AuthorFactory, ProductFactory


class IndexPageTests(TestCase):
    def test_index_page_title(self):
        response = self.client.get(reverse("index"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "products/index.html")
        self.assertEqual(response.context["title"], "Book Store")


@override_settings(
    MEDIA_ROOT=settings.BASE_DIR / "products/tests/test_data/media"
)
class ProductsPageTests(TestCase):
    def setUp(self):
        self.author = AuthorFactory()
        self.product = ProductFactory.create(
            category__name="Test category",
            name="Test product",
            author=[self.author],
        )

    def tearDown(self):
        self.product.image.delete()
        self.product.category.delete()
        self.product.publisher.delete()
        for author in self.product.author.all():
            author.delete()

    def test_products_page_has_product_and_category_in_context(self):
        response = self.client.get(reverse("products:index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "products/products.html")
        self.assertEqual(response.context["title"], "Каталог")
        self.assertEqual(
            response.context["object_list"][0].name, "Test product"
        )
        self.assertEqual(
            response.context["categories"][0].name, "Test category"
        )

    def test_products_page_has_product_from_category_in_context(self):
        response = self.client.get(
            reverse(
                "products:category", kwargs={"category_slug": "test-category"}
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "products/products.html")
        self.assertEqual(response.context["title"], "Каталог")
        self.assertEqual(
            response.context["object_list"][0].name, "Test product"
        )
        self.assertEqual(
            response.context["object_list"][0].category.name, "Test category"
        )
        self.assertEqual(
            response.context["object_list"][0].category.slug, "test-category"
        )


# TODO написать тесты на ProductDetailView (страница товара с подробностями)
