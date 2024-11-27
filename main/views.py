from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Product, Category, Specification, Team, Services, Contact, Comments, Cart, CartItem, Order, ShippingAddress
from accounts.models import Customer
# Create your views here.


class HomePageView(View):
    def get(self, request):
        
        query = request.GET.get('q', '')
        results = Product.objects.filter(title__icontains=query)
        
        data = {
            "products": Product.objects.all(),
            "services": Services.objects.all(),
            "contacts": Contact.objects.all(),
            "results": results,
            "query": query,
      
            "count_contacts": Contact.objects.count(),
            "count_products": Product.objects.count(),
            "count_customers": Customer.objects.count()
        }
        return render(request, 'index.html', context=data)
    

class AboutPageView(View):
    def get(self, request):
        data = {
            "title": "About Us",
            'last_product': Product.objects.last(),
            'team': Team.objects.all()
        }
        return render(request, 'about.html', context=data)
    

class ProductPageView(View):
    def get(self, request):
        products = Product.objects.all()

        query = request.GET.get('q', '')
        results = Product.objects.filter(title__icontains=query)

        data = {
            "title": "Shop",
            'products': products,
            'results': results,
            'last_product': Product.objects.last()
        }
        return render(request, 'product.html', context=data)


class ServicesPageView(View):
    def get(self, request):
        data = {
            "title": "Our Services",
            'last_product': Product.objects.last(),
            'services': Services.objects.all()
        }
        return render(request, 'services.html', context=data)


class ContactPageView(View):
    def get(self, request):
        data = {
            "title": "Contact Us",
            'last_product': Product.objects.last(),
            'address': "Uzbekistan, Fergana",
            'street': "Oybek",
            "phone": "+998(77)317-0154",
            "email_address": "aristokrat_shop24@gmail.com",
            "official_site": "aristokrat_shop.com"
        }
        return render(request, 'contact.html', context=data)
    
    def post(self, request):
        firstname = request.POST.get("firstname")
        lastname = request.POST.get("lastname")
        email = request.POST.get("email")
        summary = request.POST.get("summary")
        message = request.POST.get("message")
        
        if not all([firstname, lastname, email, summary, message]):
            messages.warning(request, "Hamma maydon to'ldirilishi shart!")
            return redirect('contact')
        Contact.objects.create(firstname=firstname, lastname=lastname, email=email, summary=summary, message=message)
        messages.success(request, "Habaringiz yuborildi!")
        return redirect('home')


class SinglePageView(View):
    def get(self, request, product_id):
        product = Product.objects.get(id=product_id)
        specifications = Specification.objects.filter(product=product)

        comments = product.comments.all()

        data = {
            "title": "Product Details",
            "product": product,
            "specification": specifications,
            "comments": comments
        }
        return render(request, 'single.html', context=data)
    

class CommentPageView(LoginRequiredMixin ,View):

    login_url = '/accounts/login/'

    def get(self, request, product_id):
        product = Product.objects.get(id=product_id)
        return render(request, "add_comment.html", context={"product": product})
    
    def post(self, request, product_id):
        product = Product.objects.get(id=product_id)
        customer = Customer.objects.get(user=request.user.id)

        comment = request.POST.get("comment")

        if comment:
            Comments.objects.create(author=customer, description=comment, product=product)
            return redirect("single", product_id=product.id)
        return render(request, "add_comment.html", context={"product": product, "error": "Maydon bo'sh bo'lishi mumkin emas!"})


class CartView(View):
    def get(self, request):
        customer = Customer.objects.get(user=request.user.id)
        cart, created = Cart.objects.get_or_create(customer=customer, complete=False)
        cart_items = cart.cartitem_set.all()

        total_price = sum([item.get_total() for item in cart_items])

        data = {
            'cart': cart,
            'cart_items': cart_items,
            'total_price': total_price
        }
        return render(request, 'shopping/cart.html', context=data)


class AddToCartView(View):
    def post(self, request, product_id):
        customer = Customer.objects.get(user=request.user.id)
        product = Product.objects.get(id=product_id)
        cart, created = Cart.objects.get_or_create(customer=customer, complete=False)

        if CartItem.objects.filter(cart=cart, product=product).exists():
            cart_item = CartItem.objects.get(cart=cart, product=product)
            cart_item.quantity += 1
            cart_item.save()
            messages.success(request, f"{product.title} +1")
        else:
            CartItem.objects.create(cart=cart, product=product, quantity=1)
            messages.success(request, f"{product.title} savatchaga qo'shildi.")
        return redirect('cart_page')
    

class UpdateCartView(View):
    def post(self, request, cart_item_id):
        cart_item = get_object_or_404(CartItem, id=cart_item_id)

        action = request.POST.get('action')
        if action == 'plus':
            cart_item.quantity += 1
        if action == 'minus' and cart_item.quantity > 1:
            cart_item.quantity -= 1
        cart_item.save()

        return redirect('cart_page')
    

class RemoveCartItem(View):
    def post(self, request, cart_item_id):
        cart_item = CartItem.objects.get(id=cart_item_id)
        cart_item.delete()
        messages.success(request, f"{cart_item.product.title} Savatchadan o'chirildi!")
        return redirect('cart_page')
    

class CheckOutView(View):
    def get(self, request):
        customer = Customer.objects.get(user=request.user)
        cart = Cart.objects.get(customer=customer, complete=False)
        order, created = Order.objects.get_or_create(customer=customer, cart=cart, complete=False)
        data = {
            'cart': cart,
            'order': order
        }
        return render(request, 'shopping/cart.html', context=data)
    
    def post(self, request):
        customer = Customer.objects.get(user=request.user.id)
        cart = Cart.objects.get(customer=customer, complete=False)
        order, created = Order.objects.get_or_create(customer=customer, cart=cart, complete=False)
        order.complete = True
        cart.complete = True
        order.save()
        cart.save()

        messages.success(request, "Buyurtma muvaffaqiyatli yakunlandi!")
        return redirect("home")


class ShippingView(View):
    def get(self, request):
        customer = Customer.objects.get(user=request.user)
        cart = Cart.objects.get(customer=customer, complete=True)
        data = {
            "cart": customer,
            "order": cart
        }
        return render(request, 'shopping/shipping.html', context=data)
    
    def post(self, request):
        address = request.POST.get('address')
        city = request.POST.get('city')
        phone_number = request.POST.get('phone-number')

        customer = Customer.objects.get(user=request.user)
        cart = Cart.objects.get(customer=customer)

        if not all([address, city]):
            messages.warning(request, "Maydonlar to'ldirilishi shart!")
            return redirect('shipping')

        ShippingAddress.objects.create(customer=customer, cart=cart, address=address, city=city, phone_number=phone_number)
        messages.success(request, "Buyurtmangiz qabul qilindi!")
        return redirect('home')

