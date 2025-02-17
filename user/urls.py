from django.urls import path
from user import views

app_name = "user" 

urlpatterns = [
    path('', views.customer_list, name='customer-list'),
    path("customer/<int:pk>/", views.customer_detail, name="customer-details"),
    path('customer-create/', views.add_customer, name='add-customer'),
    path('customer-update/<int:pk>/', views.update_customer, name='customer-update'),      
    path('customer-delete/<int:pk>/', views.delete_customer, name='delete-customer'),
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_page, name='logout'),
    path('register/', views.register, name='register'),
]
