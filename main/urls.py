from django.urls import path

from .views import (HomePageView, ProductPageView, ServicesPageView, 
                    ContactPageView, AboutPageView, SinglePageView, 
                    CommentPageView, CartView, AddToCartView,
                    CheckOutView, RemoveCartItem, UpdateCartView)


urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('shop/', ProductPageView.as_view(), name='shop'),
    path('services/', ServicesPageView.as_view(), name='services'),
    path('contact/', ContactPageView.as_view(), name='contact'),
    path('about/', AboutPageView.as_view(), name='about'),
    path('single/<int:product_id>/', SinglePageView.as_view(), name='single'),
    path('add_comment/<int:product_id>', CommentPageView.as_view(), name="add_comment"),

    # Shopping
    path('shopping/cart', CartView.as_view(), name='cart_page'),    
    path('shopping/add-to-cart/<int:product_id>/', AddToCartView.as_view(), name="add-to-cart"),
    path('shopping/checkout', CheckOutView.as_view(), name='check-out'),
    path('shopping/delete-cart/<int:cart_item_id>/', RemoveCartItem.as_view(), name='delete-cart'),
    path('shopping/update-cart/<int:cart_item_id>/', UpdateCartView.as_view(), name="update-cart"),
]