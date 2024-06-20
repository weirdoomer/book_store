from django.core.files import File

from products.models import Product, ProductCategory


class ProductHelpersMixin:
    def create_product_with_category(
        self, product_name, category_name, with_image=True
    ):
        if with_image:
            image_path = "products/tests/test_data/test_img.jpeg"
            image_name = "test_img.jpeg"

            self.category = ProductCategory.objects.create(name=category_name)
            self.product = Product(
                name=product_name,
                description="Test description",
                price=0.00,
                category=self.category,
            )
            with open(image_path, "rb") as f:
                pic = File(f, image_name)
                self.product.image = pic
                self.product.save()
        else:
            self.category = ProductCategory.objects.create(name=category_name)
            self.product = Product(
                name=product_name,
                description="Test description",
                price=0.00,
                category=self.category,
            )
            self.product.save()


class ProductCategoryHelpersMixin:
    def create_category(self, name, slug=None):
        self.category = ProductCategory.objects.create(name=name, slug=slug)
