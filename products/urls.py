from django.urls import path, re_path

from .views import ProductsListView

app_name = "products"

urlpatterns = [
    path("", ProductsListView.as_view(), name="index"),
    path(
        "category/<slug:category_slug>/",
        ProductsListView.as_view(),
        name="category",
    ),
]
