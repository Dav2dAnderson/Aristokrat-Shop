from django.contrib import admin

from .models import *
# Register your models here.


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'price', 'image')


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('customer', 'date_added', 'complete')


@admin.register(Specification)
class SpecificationAdmin(admin.ModelAdmin):
    list_display = ('product', 'content')


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('product', 'cart', 'quantity', 'added_date')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('customer', 'cart', 'date_ordered', 'complete')


@admin.register(ShippingAddress)
class ShipAddressAdmin(admin.ModelAdmin):
    list_display = ('customer', 'order', 'city', 'address', 'date_added', 'postal_code')


@admin.register(Services)
class ServicesAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')


@admin.register(Team)
class ServicesAdmin(admin.ModelAdmin):
    list_display = ('fullname', 'job')  


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('firstname', 'lastname', 'email', 'summary')


@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ('author', 'product', 'description', 'created_at')

