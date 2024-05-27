from django.db import models

from .utils import image_resize


class ProductCategory(models.Model):
    name = models.CharField(max_length=128, unique=True)

    class Meta:
        verbose_name = "category"
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=256, unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=14, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    image = models.ImageField(
        max_length=256, upload_to="products_images", null=True, blank=True
    )
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "product"
        verbose_name_plural = "products"

    def get_product_img_url(self):
        try:
            return self.image.url
        except ValueError:
            return None

    def save(self, *args, **kwargs):
        self.image = image_resize(self.image)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Product: {self.name} | Category: {self.category.name}"
