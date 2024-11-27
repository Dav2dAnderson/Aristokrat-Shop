from django.db import models
from django.utils.text import slugify

from accounts.models import Customer

import random
# Create your models here.


class Category(models.Model):
    title = models.CharField(max_length=150)
    slug = models.SlugField(null=True, blank=True, max_length=250)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.title


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    image = models.ImageField(upload_to='product_images/', null=True, blank=True)
    title = models.CharField(max_length=250)
    description = models.TextField()
    price = models.IntegerField()

    def __str__(self) -> str:
        return self.title


class Specification(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    content = models.TextField()

    def __str__(self) -> str:
        return self.product.title
    

class Cart(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"Cart for {self.customer.fullname}"

    def get_cart_total(self):
        cart_items = self.cartitem_set.all()
        total = sum([item.get_total() for item in cart_items]) 
        return total

    def get_cart_items(self):
        cart_items = self.cartitem_set.all()
        total = sum([item.quantity for item in cart_items])
        return total


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.product.title if self.product else 'No product'} {self.quantity}"

    def get_total(self):
        if self.product:
            return self.product.price * self.quantity    
        return 0

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.SET_NULL, null=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.customer.fullname

    def get_order_total(self):
        return self.cart.get_cart_total()

    def get_order_items(self):
        return self.get_order_items()


class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    address = models.CharField(max_length=250)
    city = models.CharField(max_length=150)
    postal_code = models.CharField(max_length=10, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.customer.fullname

    def save(self, *args, **kwargs):
        if not self.postal_code:
            self.postal_code = self.generate_code()
        super().save(*args, **kwargs)

    def generate_code(self):
        return str(random.randint(10000, 99999))
    

class Services(models.Model):
    image = models.ImageField(upload_to="services_image/", null=True, blank=True)
    title = models.CharField(max_length=250)
    slug = models.SlugField(null=True, blank=True, max_length=250)
    description = models.TextField()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)


class Team(models.Model):
    image = models.ImageField(upload_to='teammate_images/', null=True, blank=True)
    fullname = models.CharField(max_length=150)
    job = models.CharField(max_length=150)
    description = models.TextField()

    def __str__(self) -> str:
        return self.fullname
    

class Contact(models.Model):
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    email = models.EmailField(max_length=150)
    summary = models.CharField(max_length=250)
    message = models.TextField()

    def __str__(self) -> str:
        return self.firstname
    

class Comments(models.Model):
    description = models.TextField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(Customer, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.author.user.username


