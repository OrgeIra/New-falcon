from django.shortcuts import render, get_object_or_404, redirect
from .forms import ReviewForm
from ecommerce.models import Product, ProductAttribute
from django.core.paginator import Paginator



def product_list(request):
    products = Product.objects.all()

    paginator = Paginator(products, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
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
