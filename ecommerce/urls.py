from django.urls import path
from .views import ProductListView, ProductDetailView

app_name = "ecommerce"

urlpatterns = [
    path("", ProductListView.as_view(), name="product_list"),
    path("product_detail/<int:pk>/", ProductDetailView.as_view(), name="product_detail"),
]
