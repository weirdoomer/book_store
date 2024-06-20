from django.conf import settings
from django.test import TestCase, override_settings
from PIL import Image

from products.tests.tests_helpers.products_test_helpers import (
    ProductCategoryHelpersMixin,
    ProductHelpersMixin,
)


class ProductCategoryModelTests(TestCase, ProductCategoryHelpersMixin):
    def tearDown(self):
        self.category.delete()

    def test_create_category_with_slug(self):
        self.create_category(name="Тестовая категория")
        self.assertEqual("Тестовая категория", self.category.name)
        self.assertEqual("testovaya-kategoriya", self.category.slug)

    def test_change_category_name_and_recreate_slug(self):
        self.create_category(name="Тестовая категория")
        self.category.name = "Измененная тестовая категория"
        self.category.save()
        self.assertEqual("Измененная тестовая категория", self.category.name)
        self.assertEqual(
            "izmenennaya-testovaya-kategoriya", self.category.slug
        )

    def test_create_category_with_name_from_symbols(self):
        self.create_category(name="!@#$%^&*()_+")
        self.assertEqual("!@#$%^&*()_+", self.category.name)
        self.assertIn("default_slug_", self.category.slug)


@override_settings(
    MEDIA_ROOT=settings.BASE_DIR / "products/tests/test_data/media"
)
class ProductModelTests(TestCase, ProductHelpersMixin):
    def tearDown(self):
        self.product.image.delete()
        self.category.delete()

    def test_resize_and_save_img(self):
        product_name = "Test product"
        category_name = "Test category"
        self.create_product_with_category(
            product_name=product_name, category_name=category_name
        )

        pic_size = (367, 507)
        pic_format = "WEBP"

        with Image.open(self.product.image) as product_image:
            product_image.load()

        self.assertTupleEqual(product_image.size, pic_size)
        self.assertEqual(product_image.format, pic_format)

    def test_get_product_img_url_with_image(self):
        product_name = "Test product"
        category_name = "Test category"
        self.create_product_with_category(
            product_name=product_name, category_name=category_name
        )

        expected_url = "/media/products_images/test_img.webp"
        self.assertEqual(self.product.get_product_img_url(), expected_url)

    def test_get_product_img_url_without_image(self):
        product_name = "Test product"
        category_name = "Test category"
        self.create_product_with_category(
            product_name=product_name,
            category_name=category_name,
            with_image=False,
        )

        expected_url = None
        self.product.image.delete()
        self.assertEqual(self.product.get_product_img_url(), expected_url)

    def test_create_product_with_slug(self):
        product_name = "Test product"
        category_name = "Test category"
        self.create_product_with_category(
            product_name=product_name, category_name=category_name
        )
        self.assertEqual(product_name, self.product.name)
        self.assertEqual("test-product", self.product.slug)

    def test_change_product_name_and_recreate_slug(self):
        product_name = "Test product"
        category_name = "Test category"
        self.create_product_with_category(
            product_name=product_name,
            category_name=category_name,
            with_image=False,
        )
        self.product.name = "Измененное имя продукта"
        self.product.save()
        self.assertEqual("Измененное имя продукта", self.product.name)
        self.assertEqual("izmenennoe-imya-produkta", self.product.slug)

    def test_create_product_with_name_from_symbols(self):
        product_name = "!@#$%^&*()_+"
        category_name = "Test category"
        self.create_product_with_category(
            product_name=product_name, category_name=category_name
        )
        self.assertEqual(product_name, self.product.name)
        self.assertIn("default_slug_", self.product.slug)
