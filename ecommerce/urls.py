from django.urls import path
from ecommerce import views

app_name = "ecommerce"

urlpatterns = [
    path("", views.product_list, name="product_list"),
    path("product_detail/<int:pk>/", views.product_detail, name="product_detail"),
]
