from django.conf import settings
from django.test import TestCase, override_settings
from PIL import Image

from products.tests.tests_helpers.products_test_helpers import (
    ProductsHelpersMixin,
)


@override_settings(
    MEDIA_ROOT=settings.BASE_DIR / "products/tests/test_data/media"
)
class ProductModelTests(TestCase, ProductsHelpersMixin):
    def tearDown(self):
        self.product.image.delete()
        self.category.delete()

    def test_resize_and_save_img(self):
        self.create_product()

        pic_size = (367, 507)
        pic_format = "WEBP"

        with Image.open(self.product.image) as product_image:
            product_image.load()

        self.assertTupleEqual(product_image.size, pic_size)
        self.assertEqual(product_image.format, pic_format)

    def test_get_product_img_url_with_image(self):
        self.create_product()

        expected_url = "/media/products_images/test_img.webp"
        self.assertEqual(self.product.get_product_img_url(), expected_url)

    def test_get_product_img_url_without_image(self):
        self.create_product(with_image=False)

        expected_url = None
        self.product.image.delete()
        self.assertEqual(self.product.get_product_img_url(), expected_url)
