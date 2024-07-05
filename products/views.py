from django.shortcuts import render
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from common.utils.views.views_mixins import TitleMixin

from .models import Product, ProductCategory


class IndexView(TitleMixin, ListView):
    model = Product
    template_name = "products/index.html"
    ordering = "name"
    paginate_by = 12
    title = "Book Store"


class ProductsListView(TitleMixin, ListView):
    model = Product
    template_name = "products/products.html"
    ordering = "name"
    paginate_by = 8
    title = "Каталог"

    def get_queryset(self):
        queryset = super().get_queryset()
        category_slug = self.kwargs.get("category_slug")
        return (
            queryset.filter(category__slug=category_slug)
            if category_slug
            else queryset
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context["categories"] = ProductCategory.objects.all()
        return context


class ProductDetailView(TitleMixin, DetailView):
    model = Product
    template_name = "products/product.html"
    slug_field = "slug"

    def get_title(self):
        authors_str = ", ".join(
            [f"{i.first_name} {i.last_name}" for i in self.object.author.all()]
        )
        return f"{self.object.name} ({authors_str})"
