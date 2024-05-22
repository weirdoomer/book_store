from django.contrib import admin

from products.models import Product, ProductCategory


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ["name"]
    fields = ["name"]
    search_fields = ["name"]
    ordering = ["name"]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "price", "quantity", "category"]
    fields = [
        "name",
        "description",
        ("price", "quantity"),
        "image",
        "category",
    ]
    search_fields = ["name"]
    ordering = ["name"]
