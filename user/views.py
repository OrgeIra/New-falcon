from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import get_user_model
from user.forms import UserForm, LoginForm, RegisterForm
from django.http import HttpResponseNotFound
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.urls import reverse


User = get_user_model() 


def customer_list(request):
    users = User.objects.all()
    context = {
        'users': users,
    }
    return render(request, 'user/customer_list.html', context)


def customer_detail(request, pk):
    user = get_object_or_404(User, id=pk)
    context = {
        'user': user,
    }
    return render(request, 'user/customer-details.html', context)


def add_customer(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user:customer-list')
    else:
        form = UserForm()
    context = {
        'form': form,
    }
    return render(request, 'user/add_customer.html', context)


def update_customer(request, pk):
    user = get_object_or_404(User, id=pk)
    form = UserForm(instance=user)
    
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user:customer-details', pk=pk)
    
    context = {
        "form": form,
        "user": user,
    }
    return render(request, "user/edit_customer.html", context)


def delete_customer(request, pk):
    try:
        user = User.objects.get(id=pk)
        print(f"User found: {user}")
    except User.DoesNotExist:
        print(f"User with ID {pk} does not exist")
        return HttpResponseNotFound(f"User with ID {pk} does not exist")

    if request.method == 'POST':
        user.delete()
        return redirect('user:customer-list')

    context = {'user': user}
    return render(request, 'user/delete_customer.html', context)



def login_page(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user:
                login(request, user)
                return redirect('ecommerce:''')
            else:
                messages.add_message(request, messages.ERROR, 'Invalid login')
    context = {
        'form': form
    }
    return render(request, 'users/login.html', context=context)


def logout_page(request):
    logout(request)
    return redirect('user:logout')

# user/views.py

def register(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('some_success_url')
    return render(request, 'user/register.html', {'form': form})
