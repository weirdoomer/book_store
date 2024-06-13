from django.conf import settings
from django.test import TestCase, override_settings
from django.urls import reverse

from products.tests.tests_helpers.products_test_helpers import (
    ProductHelpersMixin,
)


@override_settings(
    MEDIA_ROOT=settings.BASE_DIR / "products/tests/test_data/media"
)
class IndexPageTests(TestCase, ProductHelpersMixin):
    def setUp(self):
        self.create_product_with_category()

    def tearDown(self):
        self.product.image.delete()
        self.category.delete()

    def test_index_page(self):
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "products/index.html")
        self.assertEqual(response.context["title"], "Book Store")


@override_settings(
    MEDIA_ROOT=settings.BASE_DIR / "products/tests/test_data/media"
)
class ProductsPageTests(TestCase, ProductHelpersMixin):
    def setUp(self):
        self.create_product_with_category()

    def tearDown(self):
        self.product.image.delete()
        self.category.delete()

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
