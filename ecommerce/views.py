from django.shortcuts import render, get_object_or_404, redirect
from .forms import ReviewForm
from ecommerce.models import Product, ProductAttribute


def product_list(request):
    products = Product.objects.all()
    context = {
        "products": products,
    }
    return render(request, "e-commerce/product/product-list.html", context=context)


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product_attributes = ProductAttribute.objects.filter(product=product)
    reviews = product.reviews.all()

    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.save()
            return redirect("ecommerce:product_detail", pk=pk)

    else:
        form = ReviewForm()

    context = {
        "product": product,
        "product_attributes": product_attributes,
        "reviews": reviews,
        "form": form,
    }

    return render(request, "e-commerce/product/product-details.html", context)
