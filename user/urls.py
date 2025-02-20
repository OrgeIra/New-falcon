from django.urls import path
from .views import (
    CustomerListView, CustomerDetailView, AddCustomerView, 
    UpdateCustomerView, DeleteCustomerView, LoginPageView, 
    LogoutPageView, RegisterView
)

app_name = "user"

urlpatterns = [
    path("customers/", CustomerListView.as_view(), name="customer-list"),
    path("customers/<int:pk>/", CustomerDetailView.as_view(), name="customer-details"),
    path("customers/add/", AddCustomerView.as_view(), name="add-customer"),
    path("customers/<int:pk>/edit/", UpdateCustomerView.as_view(), name="update-customer"),
    path("customers/<int:pk>/delete/", DeleteCustomerView.as_view(), name="delete-customer"),
    path("login/", LoginPageView.as_view(), name="login"),
    path("logout/", LogoutPageView.as_view(), name="logout"),
    path("register/", RegisterView.as_view(), name="register"),
]
