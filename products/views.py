from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic.list import ListView

from .models import Product, ProductCategory


class IndexView(ListView):
    model = Product
    template_name = "products/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context["title"] = "Book Store"
        return context
