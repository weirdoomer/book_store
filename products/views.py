from django.shortcuts import render
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
        category_id = self.kwargs.get("category_id")
        return (
            queryset.filter(category_id=category_id)
            if category_id
            else queryset
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context["categories"] = ProductCategory.objects.all()
        return context
