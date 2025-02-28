from django.urls import path
from .views import (
    CustomerListView,
    CustomerDetailView,
    AddCustomerView,
    UpdateCustomerView,
    DeleteCustomerView,
    LoginPageView,
    RegisterPage,
    custom_logout,
    verify_email_complete,
    verify_email_confirm,
    export_data,
    send_email,
    register_page,
)

app_name = "user"

urlpatterns = [
    path("", CustomerListView.as_view(), name="customer-list"),
    path("customers/<int:pk>/", CustomerDetailView.as_view(), name="customer-details"),
    path("customers/add/", AddCustomerView.as_view(), name="add-customer"),
    path("customers/<int:pk>/edit/", UpdateCustomerView.as_view(), name="update-customer"),
    path("customers/<int:pk>/delete/", DeleteCustomerView.as_view(), name="delete-customer"),
    path("login/", LoginPageView.as_view(), name="login"),
    path("logout/", custom_logout, name="logout"),
    path('register/', register_page, name='register_page'),
    path("verify-email/<uidb64>/<token>/", verify_email_confirm, name="verify-email"),
    path("verify-email/complete/", verify_email_complete, name="verify-email-complete"),
    path("export-data/", export_data, name="export-data"),
    path("send-email/", send_email, name="send-email"),
]
