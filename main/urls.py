from django.urls import path

from .views import main, ded, register

urlpatterns = [
    path("", main),
    path("ded", ded),
    path("register", register),
]
