from django.contrib import admin

from products.models import Author, Product, ProductCategory, Publisher


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ["last_name", "first_name"]
    fields = ["first_name", "last_name"]
    search_fields = ["last_name"]
    ordering = ["last_name"]


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
