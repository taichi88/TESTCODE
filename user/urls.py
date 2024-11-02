from . import views

from django.urls import path



urlpatterns = [
    path("register/", views.register, name="register"),
    path("login/", views.Login.as_view(), name="login"),
    path("logout/", views.Logout.as_view(), name="logout")


] 