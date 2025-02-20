from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormMixin
from django.core.paginator import Paginator
from .forms import ReviewForm
from ecommerce.models import Product, ProductAttribute


class ProductListView(ListView):
    model = Product
    template_name = "e-commerce/product/product-list.html"
    context_object_name = "page_obj"
    paginate_by = 1  # Items per page

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_obj"] = self.get_queryset()  # Ensure pagination
        return context


class ProductDetailView(FormMixin, DetailView):
    model = Product
    template_name = "e-commerce/product/product-details.html"
    context_object_name = "product"
    form_class = ReviewForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        context["product_attributes"] = ProductAttribute.objects.filter(product=product)
        context["reviews"] = product.reviews.all()
        context["form"] = self.get_form()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            review = form.save(commit=False)
            review.product = self.object
            review.save()
            return redirect("ecommerce:product_detail", pk=self.object.pk)
        return self.get(request, *args, **kwargs)
