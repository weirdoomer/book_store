from django.conf import settings
from django.test import TestCase, override_settings
from django.urls import reverse

from products.tests.tests_helpers.products_test_helpers import (
    ProductsHelpersMixin,
)


@override_settings(
    MEDIA_ROOT=settings.BASE_DIR / "products/tests/test_data/media"
)
class IndexPageTests(TestCase, ProductsHelpersMixin):
    def setUp(self):
        self.create_product()
        print(self.product.image.path)

    def tearDown(self):
        self.product.image.delete()
        self.category.delete()

    def test_index_page(self):
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "products/index.html")
        self.assertEqual(response.context["title"], "Book Store")
