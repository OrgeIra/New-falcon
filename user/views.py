from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponseNotFound
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import UserForm, LoginForm, RegisterForm


User = get_user_model()


class CustomerListView(LoginRequiredMixin, ListView):
    model = User
    template_name = "user/customer_list.html"
    context_object_name = "users"


class CustomerDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = "user/customer-details.html"
    context_object_name = "user"


class AddCustomerView(LoginRequiredMixin, CreateView):
    model = User
    form_class = UserForm
    template_name = "user/add_customer.html"
    success_url = reverse_lazy("user:customer-list")


class UpdateCustomerView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserForm
    template_name = "user/edit_customer.html"

    def get_success_url(self):
        return reverse_lazy("user:customer-details", kwargs={"pk": self.object.pk})



class DeleteCustomerView(LoginRequiredMixin, DeleteView):
    model = User
    template_name = "user/delete_customer.html"
    success_url = reverse_lazy("user:customer-list")

    def get(self, request, *args, **kwargs):
        user = self.get_object()
        if not user:
            return HttpResponseNotFound(f"User with ID {self.kwargs['pk']} does not exist")
        return super().get(request, *args, **kwargs)



class LoginPageView(FormView):
    template_name = "user/login.html"
    form_class = LoginForm

    def form_valid(self, form):
        email = form.cleaned_data["email"]
        password = form.cleaned_data["password"]
        user = authenticate(self.request, email=email, password=password)
        if user:
            login(self.request, user)
            return redirect("ecommerce:product_list")
        else:
            messages.error(self.request, "Invalid login")
            return self.form_invalid(form)


class LogoutPageView(LoginRequiredMixin, ListView):
    template_name = "user/logout.html"

    def get(self, request, *args, **kwargs):
        logout(request)
        return super().get(request, *args, **kwargs)


class RegisterView(FormView):
    template_name = "user/register.html"
    form_class = RegisterForm

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)  # Auto login after registration
        messages.success(self.request, "Registration successful!")
        return redirect("ecommerce:product_list")

    def form_invalid(self, form):
        messages.error(self.request, "Registration failed. Please correct the errors below.")
        return super().form_invalid(form)


from django.core.mail import send_mail

def send_email(request):
    send_mail(
        'Test email',
        'I am Abdusami and I am testing the email sending functionality',
        'dodomatovabdusami@gmail.com',
        ['dodomatovabdusami0@gmail.com'],
        fail_silently=False,
    )

send_mail(
    'Test Subject',
    'This is a test email from Django.',
    'dodomatovabdusami@example.com',
    ['jm1495046@gmail.com'],
    fail_silently=False,
)