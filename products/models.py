from django.db import models

from .utils import image_resize, slug_check_and_gen


class ProductCategory(models.Model):
    name = models.CharField(max_length=128, null=False, unique=True)
    slug = models.SlugField(max_length=128, null=True, unique=True)

    class Meta:
        verbose_name = "category"
        verbose_name_plural = "categories"

    def save(self, *args, **kwargs):
        slug_check_and_gen(object=self)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Publisher(models.Model):
    name = models.CharField(
        max_length=128, null=False, blank=False, unique=True
    )


class Author(models.Model):
    first_name = models.CharField(max_length=128, null=False, blank=False)
    last_name = models.CharField(max_length=128, null=False, blank=False)


class Product(models.Model):
    name = models.CharField(max_length=256, null=False, unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=14, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    image = models.ImageField(
        max_length=256, upload_to="products_images", null=True, blank=True
    )
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=256, null=True, unique=True)

    class Meta:
        verbose_name = "product"
        verbose_name_plural = "products"

    def get_product_img_url(self):
        try:
            return self.image.url
        except ValueError:
            return None

    def save(self, *args, **kwargs):
        if self.image:
            self.image = image_resize(self.image)
        slug_check_and_gen(object=self)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Product: {self.name} | Category: {self.category.name}"
