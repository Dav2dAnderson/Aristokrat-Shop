from django.urls import path

from .views import LoginPageView, RegistrationPageView, LogOutView


urlpatterns = [
    path('login/', LoginPageView.as_view(), name="login"),
    path('register/', RegistrationPageView.as_view(), name="register"),
    path('logout/', LogOutView.as_view(), name="logout")
]