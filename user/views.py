import json
import csv
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponseNotFound, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    FormView,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import UserForm, LoginForm, RegisterForm

from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from user.custom_token import account_activation_token
from django.core.mail import EmailMessage
from django.views.decorators.csrf import csrf_exempt


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
            return HttpResponseNotFound(
                f"User with ID {self.kwargs['pk']} does not exist"
            )
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


def custom_logout(request):
    logout(request)
    return redirect(reverse_lazy("user:login"))


@csrf_exempt
def register_page(request):
    form = RegisterForm()
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            email = form.cleaned_data["email"]

            user.set_password(user.password)
            user.is_active = False  
            user.save()
            
           
            current_site = get_current_site(request)
            subject = "Verify Your Email"
            message = render_to_string(
                "user/email-verification/verify_email_message.html",
                {
                    "user": user,
                    "domain": current_site.domain,
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "token": account_activation_token.make_token(user),
                },
            )

            email = EmailMessage(subject, message, to=[email])
            email.content_subtype = "html"
            email.send()

            return HttpResponse("<h2>We have sent you a verification email. Please check your inbox.</h2>")

    return render(request, "user/register.html", {"form": form})



class RegisterPage(FormView):
    template_name = 'user/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('ecommerce:product_list')

    def form_valid(self, form):
        user = form.save(commit=False)
        get_name_by_email = user.email.split('@')[0]
        user.is_staff = True
        user.is_superuser = True
        user.set_password(user.password)
        user.save()
        send_mail(
            f'{get_name_by_email}',
            'You successfully registered',
            DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False
        )
        login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
        return redirect(self.success_url)

    def form_invalid(self, form):
        """Return the form with errors instead of None."""
        return self.render_to_response(self.get_context_data(form=form))



def verify_email_confirm(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64)) 
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True  #
        user.save()
        messages.success(request, "Your email has been verified. You can now log in.")
        return redirect("user:login")
    else:
        messages.warning(request, "The verification link is invalid or has expired.")
        return render(request, "user/email-verification/verify_email_confirm.html")


def verify_email_complete(request):
    return render(request, 'user/email-verification/verify_email_complete.html')

def export_data(request):       
    pass
    # format = request.GET.get("format", "")
    # response = None
    # if format == "csv":
    #     response = HttpResponse(content_type="text/csv")
    #     response["Content-Disposition"] = "attachment; filename=customer_list.csv"
    #     writer = csv.writer(response)
    #     writer.writerow(["Id", "Full Name", "Email", "Phone Number", "Address"])
    #     for customer in User.objects.all():
    #         writer.writerow(
    #             [
    #                 customer.id,
    #                 customer.full_name,
    #                 customer.email,
    #                 customer.phone_number,
    #                 customer.address,
    #             ]
    #         )
    # elif format == "json":
    #     response = HttpResponse(content_type="application/json")
    #     data = list(
    #         User.objects.all().values(
    #             "full_name", "email", "address", "phone_number"
    #         )
    #     )
    #     for customer in data:
    #         customer["phone_number"] = str(customer["phone_number"])
    #     response.write(json.dumps(data, indent=3))
    #     response["Content-Disposition"] = "attachment; filename=customers.json"
    # elif format == "xlsx":
    #     pass
    # else:
    #     response = HttpResponse(status=404)
    #     response.content = "Bad request"
    # return response


from django.core.mail import send_mail


def send_email(request):
    send_mail(
        "Test Email",
        "I am Abdusami and I am testing the email sending functionality",
        "DEFAULT_FROM_EMAIL",
        ["dodomatovabdusami0@gmail.com"],
        fail_silently=False,
    )
