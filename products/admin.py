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
    filter_horizontal = ["author"]
    list_display = [
        "name",
        "slug",
        "price",
        "quantity",
        "category",
        "isbn",
        "page_count",
        "publisher",
        "publication_year",
        "get_author",
    ]
    fields = [
        "name",
        "description",
        ("price", "quantity"),
        "image",
        "category",
        "isbn",
        "page_count",
        "publisher",
        "publication_year",
        "author",
    ]
    search_fields = ["name"]
    ordering = ["name"]

    @admin.display(description="author")
    def get_author(self, instance):
        return [
            f"{author.last_name} {author.first_name}"
            for author in instance.author.all()
        ]
