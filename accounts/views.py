from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.views import View
from django.http import HttpResponseForbidden
from django.contrib import messages

from .models import Customer
from django.contrib.auth.models import User
# Create your views here.


class LoginPageView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return HttpResponseForbidden("Siz allaqachon tizimga kirgansiz!\nQaytadan kirish uchun tizimdan chiqing")
        return render(request, 'registration/login.html')

    def post(self, request):
        username = request.POST.get("username")
        password = request.POST.get("password")

        if not User.objects.filter(username=username).exists():
            messages.warning(request, "Bunday foydalanuvchi topilmadi!")
            return redirect(reverse('login'))
        user = User.objects.get(username=username)

        if not user.check_password(password):
            messages.warning(request, "Parol xato kiritildi!")
            return redirect(reverse('login'))
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Siz muvaffaqiyatli tizimga kirdingiz!")
            return redirect(reverse("home"))
        else:
            messages.error(request, "Xatolik!")
            return redirect(reverse("login"))
        

class RegistrationPageView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return HttpResponseForbidden("Qaytadan ro'yxatdan o'tish uchun tizimdan chiqing!")
        return render(request, "registration/registration.html")
    
    def post(self, request):
        username = request.POST.get('username')
        fullname = request.POST.get('fullname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password') 

        if confirm_password != password:
            messages.error(request, "Parol tasdiqlanmadi!") 
            return redirect(reverse('register'))

        if User.objects.filter(username=username).exists():
            messages.warning(request, "Ushbu username allaqachon band qilingan.")
            return redirect(reverse('register'))
        elif User.objects.filter(email=email).exists():
            messages.warning(request, "Bunday email")   
            return redirect(reverse('register'))
        
        user = User.objects.create_user(username=username, password=password, email=email)
        Customer.objects.create(user=user, fullname=fullname, email=email)
        
        messages.success(request, 'Ro\'yxatdan o\'tish muvaffaqiyatli yakunlandi')
        return redirect('login')
    

class LogOutView(View):
    def get(self, request):
        logout(request)
        return redirect('home')
    

# from twilio.rest import Client
# from django.conf import settings


# def send_sms(to_phone_number, message):
#     try:
#         client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

#         message = client.messages.create(
#             body=message,
#             from_=settings.TWILIO_PHONE_NUMBER,
#             to=to_phone_number
#         )
#         return message.sid
#     except Exception as e:
#         print(f"Xato: {e}")
#         return None

# send_sms("+998901661102", "Salom Dunyo!")

        