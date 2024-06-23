from django.contrib import admin

from products.models import Product, ProductCategory, Publisher


@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    list_display = ["name"]
    fields = ["name"]
    search_fields = ["name"]
    ordering = ["name"]


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]
    fields = ["name"]
    search_fields = ["name"]
    ordering = ["name"]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "price", "quantity", "category"]
    fields = [
        "name",
        "description",
        ("price", "quantity"),
        "image",
        "category",
    ]
    search_fields = ["name"]
    ordering = ["name"]
