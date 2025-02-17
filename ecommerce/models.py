from django.db import models
from decimal import Decimal

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Category(BaseModel):
    name = models.CharField(max_length=250, unique=True)

    def __str__(self):
        return self.name
    
class Product(BaseModel):
    class RatingChoice(models.IntegerChoices):
        ONE = 1
        TWO = 2
        THREE = 3
        FOUR = 4
        FIVE = 5

    name = models.CharField(max_length=255)
    about = models.CharField(max_length=1000, default="No description available")
    description = models.TextField(default="No description available")
    price = models.DecimalField(max_digits=14, decimal_places=2)
    discount = models.DecimalField(max_digits=14, decimal_places=1, default=0)
    image = models.ImageField(upload_to='media/products/')
    stock = models.BooleanField(default=False)
    favorite = models.BooleanField(default=False)
    quantity = models.PositiveIntegerField(default=1, null=True, blank=True)
    rating = models.PositiveIntegerField(choices=RatingChoice.choices, default=RatingChoice.ONE.value)
    shipping_costs = models.DecimalField(max_digits=14, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)

    @property
    def get_absolute_url(self):
        return self.image.url
    
    @property
    def discounted_price(self):
        if self.price > 0:
            return Decimal(self.price) * Decimal(1 - self.discount / 100)
        return Decimal(self.price).quantize(Decimal('0.001'))

    def __str__(self):
        return self.name
    
class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to='media/products/')  

    def __str__(self):
        return f"{self.product.name} - Image"

class Attribute(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class AttributeValue(models.Model):
    value = models.CharField(max_length=255)

    def __str__(self):
        return self.value

class ProductAttribute(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, related_name='product_attributes', null=True, blank=True)
    attribute = models.ForeignKey(Attribute, on_delete=models.SET_NULL, null=True, blank=True)
    attribute_value = models.ForeignKey(AttributeValue, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.product.name

class Review(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")
    user_name = models.CharField(max_length=255)  
    email = models.EmailField()
    rating = models.PositiveIntegerField(choices=[(i, f"{i}★") for i in range(1, 6)], default=5)
    review_text = models.TextField()

    def __str__(self):
        return f"{self.user_name} - {self.rating}★ - {self.product.name}"
