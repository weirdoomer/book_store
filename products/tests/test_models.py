from django.conf import settings
from django.test import TestCase, override_settings
from PIL import Image

from .tests_helpers.factories import (
    AuthorFactory,
    ProductCategoryFactory,
    ProductFactory,
    PublisherFactory,
)


class ProductCategoryModelTests(TestCase):
    def tearDown(self):
        self.category.delete()

    def test_create_category_with_slug(self):
        self.category = ProductCategoryFactory(name="Тестовая категория")
        self.assertEqual("Тестовая категория", self.category.name)
        self.assertEqual("testovaya-kategoriya", self.category.slug)

    def test_change_category_name_and_recreate_slug(self):
        self.category = ProductCategoryFactory(name="Тестовая категория")
        self.category.name = "Измененная тестовая категория"
        self.category.save()
        self.assertEqual("Измененная тестовая категория", self.category.name)
        self.assertEqual(
            "izmenennaya-testovaya-kategoriya", self.category.slug
        )

    def test_create_category_with_name_from_symbols(self):
        self.category = ProductCategoryFactory(name="!@#$%^&*()_+")
        self.assertEqual("!@#$%^&*()_+", self.category.name)
        self.assertIn("default_slug_", self.category.slug)


@override_settings(
    MEDIA_ROOT=settings.BASE_DIR / "products/tests/test_data/media"
)
class ProductModelTests(TestCase):
    def tearDown(self):
        self.product.image.delete()
        self.product.category.delete()
        self.product.publisher.delete()
        for author in self.product.author.all():
            author.delete()

    def test_resize_and_save_img(self):
        self.category = ProductCategoryFactory()
        self.author = AuthorFactory()
        self.publisher = PublisherFactory()
        self.product = ProductFactory.create(
            with_image=True, author=[self.author]
        )

        pic_size = (367, 507)
        pic_format = "WEBP"

        with Image.open(self.product.image) as product_image:
            product_image.load()

        self.assertTupleEqual(product_image.size, pic_size)
        self.assertEqual(product_image.format, pic_format)

    def test_get_product_img_url_with_image(self):
        self.category = ProductCategoryFactory()
        self.author = AuthorFactory()
        self.publisher = PublisherFactory()
        self.product = ProductFactory.create(
            with_image=True, author=[self.author]
        )

        expected_url = "/media/products_images/test_img.webp"
        self.assertEqual(self.product.get_product_img_url(), expected_url)

    def test_get_product_img_url_without_image(self):
        self.category = ProductCategoryFactory()
        self.author = AuthorFactory()
        self.publisher = PublisherFactory()
        self.product = ProductFactory.create(author=[self.author])

        expected_url = None
        self.assertEqual(self.product.get_product_img_url(), expected_url)

    def test_create_product_with_slug(self):
        self.category = ProductCategoryFactory()
        self.author = AuthorFactory()
        self.publisher = PublisherFactory()
        self.product = ProductFactory.create(
            name="Test product", author=[self.author]
        )

        self.assertEqual("test-product", self.product.slug)

    def test_change_product_name_and_recreate_slug(self):
        self.category = ProductCategoryFactory()
        self.author = AuthorFactory()
        self.publisher = PublisherFactory()
        self.product = ProductFactory.create(author=[self.author])

        self.product.name = "Измененное имя продукта"
        self.product.save()
        self.assertEqual("Измененное имя продукта", self.product.name)
        self.assertEqual("izmenennoe-imya-produkta", self.product.slug)

    def test_create_product_with_name_from_symbols(self):
        # Тест проверяет, что с именем только из символов сгенерируется
        # дефолтный слаг вида default_slug_таймштамп
        self.category = ProductCategoryFactory()
        self.author = AuthorFactory()
        self.publisher = PublisherFactory()
        self.product = ProductFactory.create(
            name="!@#$%^&*()_+", author=[self.author]
        )

        self.assertIn("default_slug_", self.product.slug)


# TODO написать тесты на OverwriteImageStorage (файлы с одним названием: старые удаляются, новые сохраняются)
