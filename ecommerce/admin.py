from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Product, Category, ProductImage, Attribute, AttributeValue, ProductAttribute, Review
from django.utils.html import format_html
from django.contrib.auth.models import User, Group


class ProductInline(admin.TabularInline):
    model = Product
    extra = 1

class ReviewInline(admin.TabularInline):
    model = Review
    extra = 1


@admin.register(Product)
class ProductModelAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'image_tag')
    search_fields = ('name', 'price')
    list_filter = ('category', 'quantity', 'rating')
    autocomplete_fields = ['category']

    inlines = [ReviewInline]  

    def image_tag(self, obj):
        return format_html('<img src="{}" style="max-width:50px; max-height:50px"/>'.format(obj.image.url))

    image_tag.short_description = 'Image'


@admin.register(Category)
class CategoryModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'product_count')
    search_fields = ('title',)

    inlines = [
        ProductInline, 
    ]

    def product_count(self, category):
        return category.product_set.count()


admin.site.register(Attribute)
admin.site.register(AttributeValue)


@admin.register(ProductAttribute)
class ProductAttributeModelAdmin(admin.ModelAdmin):
    list_display = ('get_product_name', 'attribute', 'attribute_value')
    search_fields = ('attribute__name', 'attribute_value__value')

    def get_product_name(self, obj):
        return obj.product.name if obj.product else "No Product"

    get_product_name.short_description = "Product Name"


@admin.register(Review)
class ReviewModelAdmin(admin.ModelAdmin):
    list_display = ('product', 'user_name', 'created_at', 'product_count')
    search_fields = ('user_name', 'review_text')

    def product_count(self, obj):
        return obj.product.reviews.count()

    product_count.short_description = 'Review Count'


if admin.site.is_registered(User):
    admin.site.unregister(User)
admin.site.unregister(Group)
